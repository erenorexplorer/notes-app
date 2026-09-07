import { useEffect, useRef, useState } from 'react'
import ForceGraph2D, {
  type NodeObject,
  type LinkObject,
  type ForceGraphMethods,
} from 'react-force-graph-2d'
import { Box, Button } from '@mantine/core'
import { useElementSize } from '@mantine/hooks'
import { getGraph } from '../../api/client.ts'
import type { GraphData } from '../../api/types'

import classes from './GraphView.module.css'

const HIDE_LABELS_BELOW_ZOOM = 1     // Node title length hidden when zoomed out
const HIDE_RELATION_LABELS_BELOW_ZOOM = 2.5 // hide relation labels when zoomed out
const MAX_VISIBLE_TITLE_LENGTH = 60  // Node title length before truncation
const MAX_LINE_LENGTH = 25           // Node title length before wrap
const LINK_DISTANCE = 70
const CHARGE_STRENGTH = -150         // Repulsion force between nodes, negative = more repulsion force
const CHARGE_DISTANCE_MAX = 120      // Stop repulsion at this distance

const MIN_ZOOM = 1
const MAX_ZOOM = 6

// Split a title into word-wrapped lines + a total displayed characters limit
function getTitleLines(title: string) {
  const words = title.trim().split(/\s+/).filter(Boolean)
  const lines: string[] = []

  let currentLine = ''
  let totalLength = 0
  let truncated = false

  for (const word of words) {
    const nextTotalLength =
      totalLength + (totalLength > 0 ? 1 : 0) + word.length

    if (nextTotalLength > MAX_VISIBLE_TITLE_LENGTH && totalLength > 0) {
      truncated = true
      break
    }

    totalLength = nextTotalLength

    const nextLine =
      currentLine.length > 0
        ? `${currentLine} ${word}`
        : word

    if (nextLine.length > MAX_LINE_LENGTH && currentLine.length > 0) {
      lines.push(currentLine)
      currentLine = word
    } else {
      currentLine = nextLine
    }
  }

  if (currentLine) {
    lines.push(currentLine)
  }

  if (truncated && lines.length > 0) {
    lines[lines.length - 1] += '…'
  }

  return lines
}

// Draw one graph node and its persistent title.
// PERFORMANCE NOTE (large graphs): called once per node per rendered frame.
//    Potential improvements: cache title wrapping and replace per-frame glow/shadow drawing with cached sprites.
function drawNode(
  node: NodeObject,
  ctx: CanvasRenderingContext2D,
  globalScale: number,
  hoveredNodeId: string | null,
  recentlyCreatedNodeId: string | null
) {
  if (
    globalScale < HIDE_LABELS_BELOW_ZOOM ||
    node.x === undefined ||
    node.y === undefined
  ) {
    return
  }

  const nodeX = node.x
  const nodeY = node.y
  const isHovered = String(node.id) === hoveredNodeId
  const isRecentlyCreated = String(node.id) === recentlyCreatedNodeId

  // Draw the node circle and glow.
  const nodeRadius = 4

  ctx.save()

  ctx.beginPath()
  ctx.arc(nodeX, nodeY, nodeRadius, 0, 2 * Math.PI)

  ctx.fillStyle = 'rgba(17, 40, 56, 0.75)'
  ctx.strokeStyle = '#63c7ff'
  // ctx.lineWidth = isHovered ? 1 : 0.5
  // ctx.shadowColor = '#42baff'
  // ctx.shadowBlur = isHovered ? 20 : 8
  ctx.lineWidth =
  isRecentlyCreated ? 1.5 :
  isHovered ? 1 :
  0.5                         // default appearance

  ctx.shadowColor = '#42baff'

  ctx.shadowBlur =
    isRecentlyCreated ? 30 :
    isHovered ? 20 :
    8                         // default appearance
  ctx.fill()
  ctx.stroke()

  ctx.restore()

  // Draw the wrapped title below the node.
  const fullTitle = String(
    (node as NodeObject & { title?: string }).title ?? '',
  )
  const titleLines = getTitleLines(fullTitle)

  const fontSize = 12 / globalScale
  const lineHeight = fontSize * 1.2

  ctx.save()

  ctx.font = `${fontSize}px sans-serif`
  ctx.fillStyle = '#e6e6e6'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'top'

  titleLines.forEach((line, index) => {
    ctx.fillText(
      line,
      nodeX,
      nodeY + 6 + index * lineHeight,
    )
  })

  ctx.restore()
}

function drawLinkLabel(
  link: LinkObject,
  ctx: CanvasRenderingContext2D,
  globalScale: number,
) {
  // hide relation labels when zoomed out
  if (globalScale < HIDE_RELATION_LABELS_BELOW_ZOOM) {
    return
  }

  const source = link.source
  const target = link.target

  // forcegraph resolves link endpoints into node objects with x/y positions
  if (
    typeof source !== 'object' ||
    typeof target !== 'object' ||
    source.x === undefined ||
    source.y === undefined ||
    target.x === undefined ||
    target.y === undefined
  ) {
    return
  }

  const relationType = String(
    (link as LinkObject & { relation_type?: string }).relation_type ?? '',
  )

  if (!relationType) {
    return
  }

  // place label halfway between the two linked nodes
  const midX = (source.x + target.x) / 2
  const midY = (source.y + target.y) / 2

  const fontSize = 10 / globalScale

  ctx.save()

  ctx.font = `${fontSize}px sans-serif`
  ctx.fillStyle = '#bfc7cc'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  ctx.fillText(relationType, midX, midY)

  ctx.restore()
}

type GraphViewProps = {
  recentlyCreatedNodeId: string | null    // id of recently created note for highlight
  onClearRecentNode: () => void
  onOpenNote: (noteId: string) => void    // open note view for specific note by id
}

function GraphView({ recentlyCreatedNodeId, onClearRecentNode, onOpenNote }: GraphViewProps) {
  const { ref, width, height } = useElementSize()
  const graphRef = useRef<ForceGraphMethods | undefined>(undefined)

  const [graphDataResponse, setGraphDataResponse] =
    useState<GraphData | null>(null)

  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null)

  useEffect(() => {
  async function loadGraph() {
    try {
      const graphData = await getGraph()
      setGraphDataResponse(graphData)
    } catch (error) {
      console.error(error)
    }
  }

    loadGraph()
  }, [])

  useEffect(() => {

    // only configure physics once ForceGraph has data and a measurable container
    if (!graphDataResponse || width <= 0 || height <= 0) {
      return
    }

    // reference to an object from ForceGraph, contains methods to configure d3 physics
    const graph = graphRef.current

    if (!graph) {
      return
    }

    // configure d3 physics forces
    const linkForce = graph.d3Force('link')
    const chargeForce = graph.d3Force('charge')

    linkForce?.distance(LINK_DISTANCE)

    chargeForce?.strength(CHARGE_STRENGTH)
    chargeForce?.distanceMax(CHARGE_DISTANCE_MAX)

    // restart physics to update settings
    graph.d3ReheatSimulation()
  }, [
    graphDataResponse,
    width, // width and height need to be dependencies to prevent race condition
    height,
    LINK_DISTANCE,
    CHARGE_STRENGTH,
    CHARGE_DISTANCE_MAX,
  ])

  function resetView() {
      graphRef.current?.zoomToFit(400, 40)
  }

  function handleNodeHover(node: NodeObject | null) {
    const nextHoveredNodeId =
      node ? String(node.id) : null

    if (recentlyCreatedNodeId) {
      // User hovered a different node -> stop highlighting newly added node
      if (
        nextHoveredNodeId &&
        nextHoveredNodeId !== recentlyCreatedNodeId
      ) {
        onClearRecentNode()
      }

      // User hovered the new node and then moved away from it
      if (
        nextHoveredNodeId === null &&
        hoveredNodeId === recentlyCreatedNodeId
      ) {
        onClearRecentNode()
      }
    }

    setHoveredNodeId(nextHoveredNodeId)
  }

  return (
    <Box
      ref={ref}
      h="calc(100dvh - 80px)"
      className={classes.root}
    >
      <div className={`${classes.fog} ${classes.fogOne}`} />
      <div className={`${classes.fog} ${classes.fogTwo}`} />
      {/* Wait until both the container size and graph data are available. */}
      {width > 0 && height > 0 && graphDataResponse && (
        <Box
          style={{
            position: 'relative',
            zIndex: 1,
          }}
        >
            <Button
              onClick={resetView}
              style={{
                position: 'absolute',
                top: 12,
                right: 12,
                zIndex: 2,
              }}
            >
              Reset view
            </Button>
          {/* PERFORMANCE (large graphs): force-layout ticks may become the main CPU cost.
          Could shorten/freeze the simulation or use precomputed node positions. */}
          <ForceGraph2D
            ref={graphRef}
            width={width}
            height={height}
            minZoom={MIN_ZOOM}
            maxZoom={MAX_ZOOM}
            onNodeHover={handleNodeHover}
            onNodeClick={(node) => {
              onOpenNote(String(node.id))
            }}
            nodeCanvasObjectMode={() => 'replace'}
            nodeCanvasObject={(node, ctx, globalScale) => {
              drawNode(node, ctx, globalScale, hoveredNodeId, recentlyCreatedNodeId)
            }}
            // draw relation text after ForceGraph draws the normal link
            linkCanvasObjectMode={() => 'after'}
            linkCanvasObject={(link, ctx, globalScale) => {
              drawLinkLabel(link, ctx, globalScale)
            }}
            graphData={graphDataResponse}
            linkSource="source_id"
            linkTarget="target_id"


            linkColor={() => 'rgba(136, 136, 136, 0.45)'}
            linkWidth={1.5}

            // moving particles to show link direction
            linkDirectionalParticles={3}
            linkDirectionalParticleWidth={2}
            linkDirectionalParticleSpeed={0.001}

            backgroundColor="rgba(0, 0, 0, 0)"

          />
        </Box>
      )}
    </Box>
  )
}

export default GraphView