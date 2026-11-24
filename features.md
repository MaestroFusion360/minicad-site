# MiniCAD 0.9.25

MiniCAD combines 2D CAD and technical drawings, direct B-Rep solid modeling, milling CAM, two-axis turning CAM, contour cutting, and a headless command-line interface.

The CAM picker has 17 templates: nine Milling, seven Turning and one Cutting.
Version 0.9.25 is the current release; maintenance addresses confirmed defects.

## 2D CAD

Create, edit, measure, and organize precise DXF geometry with numerical input, snapping, layers, and document-level undo/redo.

| Capability | Description |
| --- | --- |
| Geometric primitives | Points, lines, polylines with straight and bulge arc segments, rectangles, regular polygons, circles, arcs, ellipses, and cubic splines. |
| Construction geometry | Horizontal, vertical, infinite, tangent, parallel, and perpendicular lines; circles and arcs from points, radii, or angles. |
| Text | TEXT and MTEXT entities with alignment, formatting, and wrapping. |
| Numeric construction | Coordinate- and dimension-driven geometry creation. |
| Editing | Move, rotate, scale, mirror, offset, trim, break, join, fillet, chamfer, and stretch. |
| Arrays and clipboard | Rectangular and circular arrays; copy, cut, paste, and cross-document clipboard operations. |
| Geometry properties | Edit dimensions and entity parameters, including polyline vertices, spline control points, and constrained rectangle geometry. |
| Selection | Select by DXF entity type, identify coincident geometry, and change drawing order. |
| Measurement | Point distance, object length/radius/diameter, explicit circle/arc diameter, and closed-object area. |
| Object snapping | Grid, endpoints, midpoints, centers, intersections, nearest points, and other supported snap modes. |
| Coordinate systems | World coordinates and multiple local coordinate systems; metric and inch units for CAD entry and display. |
| Layers and documents | Layer visibility, locking, and properties; multiple documents and sheets with independent histories. |
| Undo and recovery | Undo/redo, transaction rollback, protected saves, document recovery, and session diagnostics. |
| DXF and CNC projects | Native DXF read/write, `.cnc` project archives combining DXF and CAM data, and DXF with a `.cam.json` sidecar. |
| Recent files | Separate drawing and STEP/STL histories; long paths are shortened in menus, with the full path available in tooltips. |
| 2D to 3D | Extrude and revolve closed profiles into STEP/STL bodies, including nested profiles; open results in 3D View. |
| STEP sections | Generate DXF sections from a STEP model at specified Z intervals. |

## Technical Drawings

Produce dimensioned, annotated, multi-sheet technical drawings and editable ISO fastener symbols.

| Capability | Description |
| --- | --- |
| Dimensions | Linear, horizontal, aligned, angular, radial, and diametral dimensions. |
| Dimension layout | Manual or automatic arrow, text, and extension placement. |
| Fits and tolerances | Fits, tolerance grades, numerical deviations, and 14 categories of geometric tolerances. |
| Surface annotations | Surface-finish symbols, unspecified roughness, datum references, and conventional metric-thread symbols. |
| Drawing annotations | Center lines, hatches, view and section designations, detail views, leaders, and position callouts. |
| Tables and title blocks | Editable technical requirements, tables, title-block attributes, and A4/A3/A2/A1 drawing frames. |
| Multiple sheets | Main and continuation sheets, sheet-specific histories, and vector printing of mixed-format drawing sets. |
| Automatic dimensions | Automatic dimension placement for recognized geometry, including hole grouping and placement diagnostics. |
| ISO fasteners | ISO 4017 bolts, ISO 4032 nuts, ISO 7089 washers, ISO 4762 socket-head screws, ISO 1207 slotted screws, and ISO 7380 button-head screws. |
| Fastener parameters | Catalogue sizes and valid lengths, front/side/both views, and conventional thread representation. |
| Editable fastener macros | Native DXF BLOCK/INSERT macro objects retain their standard, size, length, and view parameters for editing and regeneration. |
| Drawing formatting | Apply drawing formats across open documents as a grouped operation. |

## 3D View

Model and edit precise OpenCascade B-Rep solids, inspect STEP assemblies, view STL meshes, and transfer geometry to CAD or CAM.

| Capability | Description |
| --- | --- |
| STEP and STL import | STEP/XCAF B-Rep assemblies with component hierarchy, names, colors, placement, and materials; multiple STL meshes for viewing. |
| 3D primitives | Box, cylinder, sphere, cone, torus, prism, and pyramid. |
| Primitive placement | XY/XZ/YZ planes or a selected planar face, with local XYZ offsets and signed extrusion direction. |
| Transformations | Position, rotate, mirror, and scale with a selectable base point. |
| Boolean operations | Union, subtract, and intersect exact B-Rep solids. |
| Edge operations | Exact B-Rep fillets and chamfers, including two-distance chamfers using a reference face. |
| Holes | Blind and through holes; entrance chamfers, counterbores, countersinks, and drill-point geometry. |
| Threaded holes | Catalogue-based thread-hole drill diameters with conventional, non-helical thread representation. |
| Arrays | Circular and two-direction rectangular arrays of bodies and selected recorded operations. |
| Sections | Display a planar section or split a B-Rep body using an X, Y, or Z plane. |
| Operation editing | Edit or delete recorded solid operations and rebuild from saved inputs where those inputs remain available. |
| Geometric selection | Select exact faces, edges, and vertices; filter by radius, length, area, normal, adjacency, range, and proximity. |
| Snaps and measurements | Snap to 3D geometric points; measure exact distances, angles, lengths, radii, areas, and coordinate differences, with a copyable result panel, in-view labels, and text toggles between Radius/Diameter and Angle/Supplement. |
| Topology tracking | Track relationships between B-Rep elements across recorded modeling steps. |
| Body properties | Dimensions, surface area, volume, mass properties, density, and assigned materials. |
| Assembly export | Export selected solids or full STEP/XCAF scenes with placements, metadata, colors, and repeated components. |
| To CAD | Generate top, bottom, front, back, left and right DXF projections plus X/Y/Z centre section outlines (no hatch) of exact B-Rep models; each selected view is centred on its own layer. |
| To CAM | Pass an oriented STEP/STL model as a reference triangle mesh into CAM, including storage inside `.cnc`; STEP/primitive bodies also get an editable `CAM_REFERENCE` top outline. |
| Display and navigation | Orthographic camera, ViewCube, solid/wireframe modes, object visibility, orbit, pan, zoom, and configurable triangulation quality. |
| Scene state | Separate scene, camera, selection, and undo/redo for each open document; crash-recovery snapshots include 3D state. |

## Milling CAM

Generate 2.5D milling paths using DXF geometry, milling tools, cutter compensation, and configurable machining parameters.

| Operation or feature | Description |
| --- | --- |
| Contour 2D | Open/closed profiles, inside/outside machining, direction, lead-in/out, side passes, and chamfer mode. |
| Pocket 2D | Closed pockets with islands, depth and lateral steps, tool-radius offsets, and nested-region handling. |
| Adaptive 2D | Engagement-based toolpaths with optimal load, finishing, connection planning, geometric tolerance, and minimum cutting radius. |
| Open Pocket | A simple U-shaped wall without Setup, or an unambiguous region bounded by Setup stock and selected open walls, including internal islands. |
| Rest Milling | Geometric remaining-area estimation for Contour and Pocket using a preceding tool diameter and stock allowance. |
| Finish Walls | Additional nominal-wall finishing paths after rough passes in Contour and Pocket. |
| Engrave | Engraving of TEXT/MTEXT outlines. |
| Drilling | G81, G82, G83, and G84 cycles or explicit G1/G0 drilling moves; G83 uses peck depth Q and dwell P. |
| Face | Zigzag or one-way face milling. |
| Bore | Helical bore machining, bottom finishing, internal/external selection, and radial passes. |
| ThreadMill | Internal/external, right-/left-hand thread milling with helical interpolation. |
| Entry strategies | Plunge, contour ramp, linear ramp, pocket helix, and center entry where supported. |
| Machining parameters | Stepdown, stepover, stock allowances, feed rates, spindle speed, safe Z, coolant, and tool selection. Side stepover defaults to 40% of the tool diameter and accepts up to the full diameter. |
| Toolpath Length | The Operations table shows the total feed-move length before Time, excluding G0 rapids and including exact native arc lengths. |
| Geometry and safety checks | Tool clearance, admissible entry paths, profile validation, arc handling, and stale-result detection. |
| Path regeneration | Recalculate stored operations from their source geometry and parameters. |

## Tool Library

Keep milling cutters and turning inserts in one persistent library that can be exchanged as JSON.

| Capability | Description |
| --- | --- |
| Milling tools | Milling tool table with tool numbers T/H/D. |
| Turning inserts | Turning insert types and orientation information. |
| Shared library | Milling and turning share the same persistent tool library. |
| JSON exchange | Import and export the tool library as JSON. |

## Turning CAM

Generate two-axis ISO lathe toolpaths for cylindrical stock, including facing, profiling, grooving, boring, and G32 thread turning.

| Operation or feature | Description |
| --- | --- |
| Turning Setup | Cylindrical stock with outside diameter, optional pilot bore, length, and front-face Z; separate turning operation category. |
| Stock selection | Select on canvas fills stock dimensions from a Z/radius rectangle relative to the selected work origin; radii are doubled into diameters. Apply saves the change as one undo/redo step. |
| Face | Face turning with explicit ISO tool movements. |
| Rough | External or accessible internal longitudinal roughing with radial steps and allowance. |
| Finish | Profile finishing in XZ with geometric insert-tip radius compensation. |
| Groove | Repeated plunges using insert width; starts at the selected groove opening with a safe approach distance. |
| Boring (ID) | Internal machining of an accessible profile with a pilot bore and suitable insert orientation. |
| Thread Turn | OD and ID straight-thread passes generated as G32 in the GUI and CLI. |
| Lathe Drilling | Ordinary or full-retract peck drilling on X0 along Z with explicit G0/G1, drill diameter/length, depth, clearance, feed, RPM, T and M3/M4; available through GUI and CLI. |
| Thread parameters | OD/ID selection, start/end Z, pitch F, radial depth P, clearance R, first-pass depth, minimum pass depth, and finishing-pass count on one dialog tab. |
| Profile input | Connected DXF LINE/ARC chains or unambiguous closed axial profiles, preserving circular arcs and the internal order of joined polyline segments. |
| Profile direction | Segment arrows remain visible on turning polyline segments before operation parameters are complete. |
| Insert geometry | 80° and 35° diamond inserts, groove and threading inserts, tip radii, orientation checks, and geometric tool preview. |
| Groove tool reference | OD P3 / ID P2 groove-tool reference convention; width extends toward +Z from the programmed front edge. |
| Turning Play | Path playback without overlay labels, showing actual-size 80°/35° diamond inserts with tip radii and groove-insert geometry. |
| Spindle and feed modes | G96/G97 constant surface speed or RPM, G50 speed limit, G98/G99 feed modes, M3/M4, and coolant. |
| ISO NC output | Fanuc Turn Type A with explicit G0/G1/G2/G3 and G32 moves, G18, diameter X, and I/K circular interpolation; G99 is set in the safety block and repeated only when the feed mode changes. |
| Tool changes | M09 / G28 U0 W0 / M01 before the next tool; end sequence M09 / G28 U0 W0 / M05 / M01 before M30. |
| Program validation | Independent checks of reference returns, working-coordinate reestablishment, geometry, and modal NC output. |

## Turning Simulation

Preview turning toolpaths in Play and check material removal in Easy G-Code Plot (EGP) before posting the NC program.

| Capability | Description |
| --- | --- |
| Turning Play | Turning path playback without overlay labels, with actual-size 80°/35° diamond inserts, tip radii, and groove-insert geometry. |
| Simulation inputs | The setup cylinder, pilot bore, and every tool used by the program are transferred to the lathe removal model. |
| EGP manifest | Manifest v2 for Milling and Turning; the matching EGP reader is required. |
| Stale toolpaths | Play and Simulate offer regeneration of outdated toolpaths, then continue the original command. |
| Scope | Cutting is excluded; built-in Play shows paths and reference models but does not remove stock or check fixture collisions. |

## Cutting CAM

Cutting is an independent CAM Setup and operation category alongside Milling and Turning.

| Capability | Description |
| --- | --- |
| Independent Setup | Select Cutting as its own setup type instead of a Milling operation. |
| Original geometry | Generate cutting movement along the source geometry without tool-radius offset. |
| Operation category | Cutting appears as a separate category in CAM operation selection. |
| Tool panel | The CAM Tools tab is unavailable for Cutting setups. |
| Viewing | Geometry and trajectories remain visible in XY; Play and EGP Simulate are disabled for Cutting. |
| Operation dialog | Tool, feed, Top Z, Bottom Z, Safe Z, coordinates, and comment; no spindle speed, plunge feed, stepdown, or coolant controls. Generation uses one pass at Bottom Z without coolant. |
| AMADA Laser | Dedicated postprocessor with beam on/off control, modal XY/feed output, and native radius arcs split into pieces of at most 90°. No milling tool changes, spindle/coolant commands, or Z moves are emitted. |
| Laser Setup | Material and thickness database codes, G92 X/Y coordinates, and program number; the same settings are available in CLI recipes. |
| Project storage | Cutting Setup and operations are saved with the project. |
| CLI | Generate and regenerate Cutting operations, export AMADA NC, and inspect exact XY movements and verification limits through `cam list --json`. |

## CAM Tools, NC and Playback

Configure tools and postprocessors, manage CAM operations, generate NC output, and inspect toolpaths.

| Capability | Description |
| --- | --- |
| CAM Setup | Milling, Turning, or Cutting machine mode, stock, program number, comments, and applicable postprocessor settings; G54–G59 for milling/turning and G92 coordinates for AMADA Laser. |
| Tool library | Milling tool table with tool numbers T/H/D; turning insert types and orientation information. |
| Spindle and coolant | Spindle direction M3/M4, speed/feed settings, tool changes, and M8/M9 coolant handling. |
| Milling postprocessors | Fanuc, Heidenhain iTNC 530, and Sinumerik 840D. |
| Turning postprocessor | Fanuc Turn Type A with modal control and independent NC-text validation. |
| Cutting postprocessor | AMADA Laser with material/thickness codes, beam control, and independent NC-text validation. |
| Postprocessor profiles | Configure supported dialect formatting, precision, spacing, comments, numbering, and arc formatting; import/export profile JSON. |
| Operation management | Reorder, select, regenerate, copy/paste between open drawings, and combine compatible operations into NC output; undo/redo CAM changes. |
| Cross-document copy | Copy selected operations with their source DXF geometry and layers; shared geometry is copied once, tool-number conflicts are resolved, the target Setup is used, and pasted operations require regeneration. |
| Generate command | Regenerate checked operations, or the selected operation, from the CAM context menu without opening an editor, as one undo/redo step. |
| Stale-path actions | Play, Postprocess, and Simulate offer regeneration of outdated toolpaths, then continue the original command. |
| Atomic recalculation | Cancellation or failure does not replace the document state or output files. |
| Diagnostics | CAM errors are shown in dialogs; regeneration prompts show the operation type for one stale operation or only the count for several. |
| NC validation | Independent geometry and formatted-NC checks, including arc precision and modal states. |
| Toolpath views | XY, XZ, and YZ projections plus interactive 3D preview of toolpaths and reference models. |
| Playback | Play, pause, stop, step controls, position slider, and traveled-path display. Milling Play interpolates G0/G1/G2/G3 continuously, shows the physical cutter at the current tip, and draws only the completed path over the opaque reference model. |
| Layer visibility | Hiding a source or generated CAM layer takes priority over CAM highlighting and hides the associated preview and trajectory. |
| External simulation | EGP manifest v2 for Milling and Turning; Turning transfers its cylinder, pilot bore and all used tools to the existing lathe removal model. Requires the matching EGP reader. Cutting is excluded; v1 is legacy. |
| Export and storage | `.cnc` archive, `.cam.json` sidecar, toolpath cache, combined NC programs, and Excel export of operations and tools. |
| NC export preferences | Output directory, optional external NC editor, and feed/arc precision limits; export rejects unrepresentable output before replacing a file. |
| Background calculation | CAM generation outside the GUI thread with cancellation and document/revision checks. |

## CLI

Use CAD, 3D geometry, CAM, and postprocessing without the graphical interface through recipe-driven commands.

| Command or area | Description |
| --- | --- |
| `inspect` | Inspect DXF/CNC documents, layers, entities, contours, inserts, and CAM operations. |
| `render` | Render a drawing to SVG. |
| `dimension` | Generate automatic drawing dimensions. |
| `cad apply` | Create and edit DXF geometry from JSON recipes. |
| `cad fasteners` | List available ISO fastener standards, sizes, and lengths. |
| `cam generate` | Generate milling, turning, and cutting operations from recipes, including Thread Turn. |
| `cam list --json` | Inspect saved operations; turning and AMADA reports include machine-readable geometry and explicit material-verification limits. |
| `cam regenerate` / `cam edit` | Regenerate and edit stored operations transactionally. |
| `cam copy` | Copy selected operations and native source geometry into another drawing, resolving tool and layer conflicts and marking pasted operations stale. |
| `cam postprocess` | Export controller-specific NC output for the supported Setup type. |
| Cutting recipes | Configure a separate `cutting` Setup with AMADA material/thickness codes and G92 coordinates. |
| `3d apply` | Create/import solids, change geometry, apply operations and arrays, and export STEP/STL/DXF. |
| `3d stats` / `3d measure` | Inspect geometry, body statistics, mass, and exact measurements. |
| `3d topology` / `3d select` | Inspect topology and select B-Rep elements using geometric criteria. |
| `3d to-cam` | Transfer a 3D model as a CAM reference mesh. |
| `batch` | Execute repeatable operations on drawing/CAM projects. |
| File protection | Check inputs and write output files transactionally. |

## Limitations

### CAD and technical drawings

- DXF is supported natively; native DWG reading and writing are not included.
- Standard fastener macros use six ISO catalogues. Studs, custom fastener catalogues, and a general sketch-constraint solver are not provided.
- Automatic dimensions apply to recognized drawing geometry, rather than every possible drawing.
- CAD can display inches, but CAM and generated NC calculations use millimetres; G20 output is not provided.

### 3D modeling and projects

- 3D View is direct B-Rep modeling, not a complete parametric CAD system with a persistent feature tree or constrained 3D sketcher.
- Editable 3D scenes are session-based. DXF and `.cnc` do not save the full editable scene; crash-recovery snapshots are not a user-facing project format.
- Boolean operations, fillets, chamfers, and holes require exact B-Rep bodies; arbitrary STL meshes are not converted into analytical solids.
- Face-based construction and holes require bounded planar faces, not arbitrary curved faces.
- Threaded holes do not contain helical thread geometry.
- Topology references track recorded operations and are not guaranteed stable after independent STEP reimport or model recreation.
- Body integrity diagnosis is available in the core/CLI; automatic B-Rep repair is not provided.
- There is no full 3D surface-machining CAM. Sending a 3D model to CAM supplies reference geometry rather than arbitrary-surface toolpaths.

### Milling, cutting and simulation

- Without Setup, Open Pocket accepts one simple U-shaped wall without islands. With Setup, wall endpoints must meet stock boundaries and the selected Left/Right side must identify one unambiguous region.
- Adaptive 2D is experimental for complex geometry.
- Rest Milling uses geometric remaining-area estimates; it does not simulate actual stock removal.
- Cutting follows original geometry with no tool offset; holding tabs and automatic nesting are not provided.
- AMADA Laser supports manual-feed through cutting. Automatic material-table feeds, etching, pierce timing, and separate files per contour are not implemented.
- AMADA export rejects helices, non-XY arcs, sloped cuts, and multiple cutting planes within one operation. Laser kerf, thermal effects, piercing, and actual material removal are not verified.
- AMADA stock Z and operation heights do not set the thickness database code or produce Z commands. Cutting Play and EGP Simulate are disabled.
- Built-in 3D Play displays paths and reference models but does not simulate stock removal or fixture collisions. Material-removal simulation is delegated to compatible EGP workflows.
- EGP manifest compatibility and simulation capabilities depend on the corresponding EGP version and supported tool types.

### Turning and NC

- Turning supports two-axis XZ geometry and the Fanuc Turn Type A dialect; live tooling, C/Y axes, and general lathe controller support are not provided.
- Turning uses explicit moves, including G32 for straight threads. Automatic G70–G76 canned turning cycles are not generated.
- Thread Turn accepts one straight axial segment and cuts toward decreasing Z (180°), with start Z greater than end Z. Tapers, arcs, and multiple source lines are rejected. Thread-form geometry and material removal are not verified.
- Turning roughing, finishing, and boring require supported, accessible profiles. Full stock removal and insert-holder/chuck collisions are not verified.
- Lathe Drilling depth ends at the drill tip. Core/CLI reports check axial paths and bounds, not complete material removal or holder/chuck clearance. EGP uses its existing drill-point stock model.
- Groove approaches the selected local opening plus clearance, assuming earlier machining has exposed it; floor-only geometry uses the Setup surface as the missing opening reference. Prior stock removal is not verified.
- Saved groove toolpaths created with the former edge convention and other outdated toolpaths require regeneration.
- Built-in postprocessor dialects and formatting profiles are provided, but arbitrary user-defined controllers (for example, dedicated Haas or Okuma profiles) are not built in.
- CAM JSON v3 is used; full compatibility with legacy v1/v2 files is not provided.
