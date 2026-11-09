# UI

> **Status:** Exploratory design sketch. This file records possible UI ideas
> for discussion; it is not an accepted specification, implementation plan, or
> backlog. Individual ideas require reconciliation with the accepted ADRs and
> explicit approval before implementation.

## Menu

* File
    * New Session
    * ---
    * Open Session
    * Save Session
    * Save As (Session)
    * ---
    * ?
* Edit
    * Undo
    * Redo
    * ---
    * Edit Data Parameters
    * Edit Object Parameters
    * ?
* Select(ion) (same as now)
* Measure
* Scene
    * Clear Scene
    * ---
    * Load Scene
    * Save Scene
    * ---
    * Add Geometry
    * Add Datastructure
    * ---
    * ?
* View (same as now)
* Help

## Sidebar

* Section 1
    * Scene Tree
    * Data store
* Section 2
    * Object: Properties of selected object(s)
    * Camera
    * Display

In the scene tree, every node provides a link to a form with two tabs: one for the scene object, one for the data item.

The tree uses icons to give an indication of the type of object.

## Toolbar

A fixed or floating toolbar provides toolbar buttons with often used tools:

* Zoom?
* Selection?
* Screen capture?
* Measurements?

## Other

The entire UI config shoould be accessible somehwere as well.
Transformations using a gimball would be amazing.
