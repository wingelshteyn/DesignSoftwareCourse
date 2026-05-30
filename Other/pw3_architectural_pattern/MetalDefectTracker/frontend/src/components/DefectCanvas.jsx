/**
 * components/DefectCanvas.jsx
 *
 * React Konva canvas that:
 *   - renders the inspection image as the bottom layer
 *   - overlays detected defect bounding boxes (excluded ones are dimmed)
 *   - overlays manually added defect boxes in a different colour
 *   - allows the operator to draw a new bbox by dragging (FRQ-7.2)
 *
 * Props:
 *   imageUrl       {string}    presigned URL to the original image
 *   detectedDefects {Array}   [{ id, defect_type, bbox_x, bbox_y, bbox_w, bbox_h, confidence }]
 *   excludedIds    {Set}       IDs of auto-detected defects that the operator excluded
 *   manualDefects  {Array}    [{ defect_type, bbox_x, bbox_y, bbox_w, bbox_h }]
 *   onAddManualDefect {fn}    callback({ defect_type, bbox_x, bbox_y, bbox_w, bbox_h })
 */

import React, { useEffect, useRef, useState } from "react";
import { Stage, Layer, Image as KonvaImage, Rect, Text } from "react-konva";
import useImage from "use-image"; // lightweight hook shipped with react-konva docs

const CANVAS_W = 800;
const CANVAS_H = 600;

const DETECTED_COLOR = "red";
const EXCLUDED_COLOR = "gray";
const MANUAL_COLOR = "blue";
const DRAW_COLOR = "green";

// Default defect type for new manually drawn boxes
const DEFAULT_DEFECT_TYPE = "other";

export default function DefectCanvas({
  imageUrl,
  detectedDefects = [],
  excludedIds = new Set(),
  manualDefects = [],
  onAddManualDefect,
}) {
  const [bgImage] = useImage(imageUrl, "anonymous");

  // Drawing state
  const isDrawing = useRef(false);
  const [drawRect, setDrawRect] = useState(null); // { x, y, w, h } in progress

  // ── Scale the image to fit the canvas ─────────────────────────────────────
  const scale =
    bgImage
      ? Math.min(CANVAS_W / bgImage.naturalWidth, CANVAS_H / bgImage.naturalHeight)
      : 1;
  const imgW = bgImage ? bgImage.naturalWidth * scale : CANVAS_W;
  const imgH = bgImage ? bgImage.naturalHeight * scale : CANVAS_H;

  // ── Mouse handlers for drawing ─────────────────────────────────────────────

  const toCanvas = (pos) => ({
    x: pos.x / scale,
    y: pos.y / scale,
  });

  const handleMouseDown = (e) => {
    const pos = e.target.getStage().getPointerPosition();
    isDrawing.current = true;
    setDrawRect({ x: pos.x, y: pos.y, w: 0, h: 0 });
  };

  const handleMouseMove = (e) => {
    if (!isDrawing.current || !drawRect) return;
    const pos = e.target.getStage().getPointerPosition();
    setDrawRect((prev) => ({
      ...prev,
      w: pos.x - prev.x,
      h: pos.y - prev.y,
    }));
  };

  const handleMouseUp = () => {
    if (!isDrawing.current || !drawRect) return;
    isDrawing.current = false;
    const { x, y, w, h } = drawRect;
    if (Math.abs(w) > 5 && Math.abs(h) > 5) {
      // Normalise negative dimensions
      const normX = w < 0 ? x + w : x;
      const normY = h < 0 ? y + h : y;
      onAddManualDefect({
        defect_type: DEFAULT_DEFECT_TYPE,
        bbox_x: normX / scale,
        bbox_y: normY / scale,
        bbox_w: Math.abs(w) / scale,
        bbox_h: Math.abs(h) / scale,
      });
    }
    setDrawRect(null);
  };

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <Stage
      width={CANVAS_W}
      height={CANVAS_H}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      style={{ cursor: "crosshair", border: "1px solid #ccc" }}
    >
      <Layer>
        {/* Background image */}
        {bgImage && (
          <KonvaImage image={bgImage} width={imgW} height={imgH} />
        )}

        {/* Auto-detected defect boxes */}
        {detectedDefects.map((d) => {
          const excluded = excludedIds.has(d.id);
          return (
            <React.Fragment key={d.id}>
              <Rect
                x={d.bbox_x * scale}
                y={d.bbox_y * scale}
                width={d.bbox_w * scale}
                height={d.bbox_h * scale}
                stroke={excluded ? EXCLUDED_COLOR : DETECTED_COLOR}
                strokeWidth={2}
                opacity={excluded ? 0.4 : 1}
              />
              <Text
                x={d.bbox_x * scale}
                y={d.bbox_y * scale - 16}
                text={`${d.defect_type} ${(d.confidence * 100).toFixed(0)}%`}
                fontSize={12}
                fill={excluded ? EXCLUDED_COLOR : DETECTED_COLOR}
                opacity={excluded ? 0.4 : 1}
              />
            </React.Fragment>
          );
        })}

        {/* Manually added defect boxes */}
        {manualDefects.map((d, i) => (
          <React.Fragment key={`manual-${i}`}>
            <Rect
              x={d.bbox_x * scale}
              y={d.bbox_y * scale}
              width={d.bbox_w * scale}
              height={d.bbox_h * scale}
              stroke={MANUAL_COLOR}
              strokeWidth={2}
              dash={[6, 3]}
            />
            <Text
              x={d.bbox_x * scale}
              y={d.bbox_y * scale - 16}
              text={d.defect_type}
              fontSize={12}
              fill={MANUAL_COLOR}
            />
          </React.Fragment>
        ))}

        {/* In-progress draw rectangle */}
        {drawRect && (
          <Rect
            x={drawRect.x}
            y={drawRect.y}
            width={drawRect.w}
            height={drawRect.h}
            stroke={DRAW_COLOR}
            strokeWidth={2}
            dash={[4, 2]}
          />
        )}
      </Layer>
    </Stage>
  );
}
