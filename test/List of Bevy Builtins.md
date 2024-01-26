Bevy Version:0.11(outdated!)


List of Bevy Builtins
This page is a quick condensed listing of all the important things provided
by Bevy.

SystemParams
Assets
File Formats
GLTF Asset Labels
Shader Imports
wgpu Backends
Schedules
Run Conditions
Plugins
Bundles
Resources (Configuration)
Resources (Engine User)

Main World
Render World
Low-Level wgpu access


Resources (Input)
Events (Input)
Events (Engine)
Events (System/Control)
Components

SystemParams
These are all the special types that can be used as system parameters.
(List in API Docs)
In regular systems:

Commands:
Manipulate the ECS using commands
Query<T, F = ()> (can contain tuples of up to 15 types):
Access to entities and components
Res<T>:
Shared access to a resource
ResMut<T>:
Exclusive (mutable) access to a resource
Option<Res<T>>:
Shared access to a resource that may not exist
Option<ResMut<T>>:
Exclusive (mutable) access to a resource that may not exist
Local<T>:
Data local to the system
EventReader<T>:
Receive events
EventWriter<T>:
Send events
&World:
Read-only direct access to the ECS World
ParamSet<...> (with up to 8 params):
Resolve conflicts between incompatible system parameters
Deferred<T>:
Custom "deferred mutation", similar to Commands, but for your own things
RemovedComponents<T>:
Removal detection
Gizmos:
A way to draw lines and shapes on the screen for debugging and dev purposes
Diagnostics:
A way to report measurements/debug data to Bevy for tracking and visualization
SystemName:
The name (string) of the system, may be useful for debugging
ParallelCommands:
Abstraction to help use Commands when you will do your own parallelism
WorldId:
The World ID of the world the system is running on
ComponentIdFor<T>:
Get the ComponentId of a given component type
Entities:
Low-level ECS metadata: All entities
Components:
Low-level ECS metadata: All components
Bundles:
Low-level ECS metadata: All bundles
Archetypes:
Low-level ECS metadata: All archetypes
SystemChangeTick:
Low-level ECS metadata: Tick used for change detection
NonSend<T>:
Shared access to Non-Send (main thread only) data
NonSendMut<T>:
Exclusive access to Non-Send (main thread only) data
Option<NonSend<T>>:
Shared access to Non-Send (main thread only) data that may not exist
Option<NonSendMut<T>>:
Exclusive access to Non-Send (main thread only) data that may not exist
StaticSystemParam:
Helper for generic system abstractions, to avoid lifetime annotations
tuples containing any of these types, with up to 16 members

In exclusive systems:

&mut World:
Full direct access to the ECS World
Local<T>:
Data local to the system
SystemState<P>:
Emulates a regular system, allowing you to easily access data from the World.
P are the system parameters.
QueryState<Q, F = ()>:
Allows you to perform queries on the World, similar to a Query
in regular systems.

Your function can have a maximum of 16 total parameters. If you need more,
group them into tuples to work around the limit. Tuples can contain up to
16 members, but can be nested indefinitely.
Systems running during the Extract schedule can also use
Extract<T>, to access data from the Main World instead of the
Render World. T can be any read-only system parameter type.
Assets
(more info about working with assets)
These are the Asset types registered by Bevy by default.

Image:
Pixel data, used as a texture for 2D and 3D rendering;
also contains the SamplerDescriptor for texture filtering settings
TextureAtlas:
2D "Sprite Sheet" defining sub-images within a single larger image
Mesh:
3D Mesh (geometry data), contains vertex attributes (like position, UVs, normals)
Shader:
GPU shader code, in one of the supported languages (WGSL/SPIR-V/GLSL)
ColorMaterial:
Basic "2D material": contains color, optionally an image
StandardMaterial:
"3D material" with support for Physically-Based Rendering
AnimationClip:
Data for a single animation sequence, can be used with AnimationPlayer
Font:
Font data used for text rendering
Scene:
Scene composed of literal ECS entities to instantiate
DynamicScene:
Scene composed with dynamic typing and reflection
Gltf:
GLTF Master Asset: index of the entire contents of a GLTF file
GltfNode:
Logical GLTF object in a scene
GltfMesh:
Logical GLTF 3D model, consisting of multiple GltfPrimitives
GltfPrimitive:
Single unit to be rendered, contains the Mesh and Material to use
AudioSource:
Audio data for bevy_audio
FontAtlasSet:
(internal use for text rendering)
SkinnedMeshInverseBindposes:
(internal use for skeletal animation)

File Formats
These are the asset file formats (asset loaders) supported by Bevy. Support
for each one can be enabled/disabled using cargo features. Some
are enabled by default, many are not.
Image formats (loaded as Image assets):
FormatCargo featureDefault?Filename extensions
PNG"png"Yes.png
HDR"hdr"Yes.hdr
KTX2"ktx2"Yes.ktx2
KTX2+zstd"ktx2", "zstd"Yes.ktx2
JPEG"jpeg"No.jpg, .jpeg
WebP"webp"No.webp
OpenEXR"exr"No.exr
TGA"tga"No.tga
PNM"pnm"No.pam, .pbm, .pgm, .ppm
BMP"bmp"No.bmp
DDS"dds"No.dds
KTX2+zlib"ktx2", "zlib"No.ktx2
Basis"basis-universal"No.basis


Audio formats (loaded as AudioSource assets):
FormatCargo featureDefault?Filename extensions
OGG Vorbis"vorbis"Yes.ogg, .oga, .spx
FLAC"flac"No.flac
WAV"wav"No.wav
MP3"mp3"No.mp3


3D asset (model or scene) formats:
FormatCargo featureDefault?Filename extensions
GLTF"bevy_gltf"Yes.gltf, .glb


Shader formats (loaded as Shader assets):
FormatCargo featureDefault?Filename extensions
WGSLn/aYes.wgsl
GLSL"shader_format_glsl"No.vert, .frag, .comp
SPIR-V"shader_format_spirv"No.spv


Font formats (loaded as Font assets):
FormatCargo featureDefault?Filename extensions
TrueTypen/aYes.ttf
OpenTypen/aYes.otf


Bevy Scenes:
FormatFilename extensions
RON-serialized scene.scn,.scn.ron


There are unofficial plugins available for adding support for even more file formats.
GLTF Asset Labels
Asset path labels to refer to GLTF sub-assets.
The following asset labels are supported ({} is the numerical index):

Scene{}: GLTF Scene as Bevy Scene
Node{}: GLTF Node as GltfNode
Mesh{}: GLTF Mesh as GltfMesh
Mesh{}/Primitive{}: GLTF Primitive as Bevy Mesh
Mesh{}/Primitive{}/MorphTargets: Morph target animation data for a GLTF Primitive
Texture{}: GLTF Texture as Bevy Image
Material{}: GLTF Material as Bevy StandardMaterial
DefaultMaterial: as above, if the GLTF file contains a default material with no index
Animation{}: GLTF Animation as Bevy AnimationClip
Skin{}: GLTF mesh skin as Bevy SkinnedMeshInverseBindposes

Shader Imports
TODO
wgpu Backends
wgpu (and hence Bevy) supports the following backends:
PlatformBackends (in order of priority)
LinuxVulkan, GLES3
WindowsDirectX 12, Vulkan, GLES3
macOSMetal
iOSMetal
AndroidVulkan, GLES3
WebWebGPU, WebGL2


On GLES3 and WebGL2, some renderer features are unsupported and performance is worse.
WebGPU is experimental and few browsers support it.
Schedules
Internally, Bevy has these built-in schedules:

Main:
runs every frame update cycle, to perform general app logic
ExtractSchedule:
runs after Main, to copy data from the Main World into the Render World
Render:
runs after ExtractSchedule, to perform all rendering/graphics, in parallel with the next Main run

The Main schedule simply runs a sequence of other schedules:
On the first run (first frame update of the app):

PreStartup
Startup
PostStartup

On every run (controlled via the MainScheduleOrder resource):

First: any initialization that must be done at the start of every frame
PreUpdate: for engine-internal systems intended to run before user logic
StateTransition: perform any pending state transitions
RunFixedUpdateLoop: runs the FixedUpdate schedule as many times as needed
Update: for all user logic (your systems) that should run every frame
PostUpdate: for engine-internal systems intended to run after user logic
Last: any final cleanup that must be done at the end of every frame

FixedUpdate is for all user logic (your systems) that should run at a fixed timestep.
StateTransition runs the
OnEnter(...)/OnTransition(...)/OnExit(...)
schedules for your states, when you want to change state.
The Render schedule is organized using sets (RenderSet):

ExtractCommands: apply deferred buffers from systems that ran in ExtractSchedule
Prepare/PrepareFlush: set up data on the GPU (buffers, textures, etc.)
Queue/QueueFlush: generate the render jobs to be run (usually phase items)
PhaseSort/PhaseSortFlush: sort and batch phase items for efficient rendering
Render/RenderFlush: execute the render graph to actually trigger the GPU to do work
Cleanup/CleanupFlush: clear any data from the render World that should not persist to the next frame

The *Flush variants are just to apply any deferred buffers after every step, if needed.
Run Conditions
TODO
Plugins
TODO
Bundles
Bevy's built-in bundle types, for spawning different common
kinds of entities.
(List in API Docs)
Any tuples of up to 15 Component types are valid bundles.
General:

SpatialBundle:
Contains the required transform and visibility
components that must be included on all entities that need rendering or hierarchy
TransformBundle:
Contains only the transform types, subset of SpatialBundle
VisibilityBundle:
Contains only the visibility types, subset of SpatialBundle

Scenes:

SceneBundle:
Used for spawning scenes
DynamicSceneBundle:
Used for spawning dynamic scenes

Audio:

AudioBundle:
Play [audio][cb::audio] from an AudioSource asset
SpatialAudioBundle:
Play positional audio from an AudioSource asset
AudioSourceBundle:
Play audio from a custom data source/stream
SpatialAudioSourceBundle:
Play positional audio from a custom data source/stream

Bevy 3D:

Camera3dBundle:
3D camera, can use perspective (default) or orthographic projection
TemporalAntiAliasBundle:
Add this to a 3D camera to enable TAA
ScreenSpaceAmbientOcclusionBundle:
Add this to a 3D camera to enable SSAO
MaterialMeshBundle:
3D Object/Primitive: a Mesh and a custom Material to draw it with
PbrBundle:
MaterialMeshBundle with the default Physically-Based Material (StandardMaterial)
DirectionalLightBundle: 
3D directional light (like the sun)
PointLightBundle: 
3D point light (like a lamp or candle)
SpotLightBundle: 
3D spot light (like a projector or flashlight)

Bevy 2D:

Camera2dBundle:
2D camera, uses orthographic projection + other special configuration for 2D
SpriteBundle: 
2D sprite (Image asset type)
SpriteSheetBundle:
2D sprite (TextureAtlas asset type)
MaterialMesh2dBundle:
2D shape, with custom Mesh and Material (similar to 3D objects)
Text2dBundle:
Text to be drawn in the 2D world (not the UI)

Bevy UI:

NodeBundle:
Empty node element (like HTML <div>)
ButtonBundle:
Button element
ImageBundle:
Image element (Image asset type)
AtlasImageBundle:
Image element (TextureAtlas asset type)
TextBundle:
Text element

Resources
(more info about working with resources)
Configuration Resources
These resources allow you to change the settings for how various parts of Bevy work.
These may be inserted at the start, but should also be fine to change at runtime (from a
system):

ClearColor:
Global renderer background color to clear the window at the start of each frame
GlobalVolume:
The overall volume for playing audio
AmbientLight:
Global renderer "fake lighting", so that shadows don't look too dark / black
Msaa:
Global renderer setting for Multi-Sample Anti-Aliasing (some platforms might only support the values 1 and 4)
UiScale:
Global scale value to make all UIs bigger/smaller
GizmoConfig:
Controls how gizmos are rendered
WireframeConfig:
Global toggle to make everything be rendered as wireframe
GamepadSettings:
Gamepad input device settings, like joystick deadzones and button sensitivities
WinitSettings:
Settings for the OS Windowing backend, including update loop / power-management settings
TimeUpdateStrategy:
Used to control how the Time is updated
Schedules:
Stores all schedules, letting you register additional functionality at runtime
MainScheduleOrder:
The sequence of schedules that will run every frame update

Settings that are not modifiable at runtime are not represented using resources. Instead,
they are configured via the respective plugins.
Engine Resources
These resources provide access to different features of the game engine at runtime.
Access them from your systems, if you need their state, or to control the respective
parts of Bevy. These resources are in the Main World. See here for the
resources in the Render World.

Time:
Global time-related information (current frame delta time, time since startup, etc.)
FixedTime:
Tracks remaining time until the next fixed update
AssetServer:
Control the asset system: Load assets, check load status, etc.
Assets<T>:
Contains the actual data of the loaded assets of a given type
State<T>:
The current value of a states type
NextState<T>:
Used to queue a transition to another state
Gamepads:
Tracks the IDs for all currently-detected (connected) gamepad devices
SceneSpawner:
Direct control over spawning Scenes into the main app World
FrameCount:
The total number of frames
ScreenshotManager:
Used to request a screenshot of a window to be taken/saved
AppTypeRegistry:
Access to the Reflection Type Registry
AsyncComputeTaskPool:
Task pool for running background CPU tasks
ComputeTaskPool:
Task pool where the main app schedule (all the systems) runs
IoTaskPool:
Task pool where background i/o tasks run (like asset loading)
WinitWindows (non-send):
Raw state of the winit backend for each window
NonSendMarker:
Dummy resource to ensure a system always runs on the main thread

Render World Resources
These resources are present in the Render World. They can be accessed
from rendering systems (that run during render stages).

MainWorld:
(extract schedule only!) access data from the Main World
RenderGraph:
The Bevy Render Graph
PipelineCache:
Bevy's manager of render pipelines. Used to store render pipelines used by the app, to avoid
recreating them more than once.
TextureCache:
Bevy's manager of temporary textures. Useful when you need textures to use internally
during rendering.
DrawFunctions<P>:
Stores draw functions for a given phase item type
RenderAssets<T>:
Contains handles to the GPU representations of currently loaded asset data
DefaultImageSampler:
The default sampler for Image asset textures
FallbackImage:
Dummy 1x1 pixel white texture. Useful for shaders that normally need a texture, when
you don't have one available.

There are many other resources in the Render World, which are not mentioned
here, either because they are internal to Bevy's rendering algorithms, or
because they are just extracted copies of the equivalent resources in the Main
World.
Low-Level wgpu Resources
Using these resources, you can have direct access to the wgpu APIs for controlling the GPU.
These are available in both the Main World and the Render World.

RenderDevice:
The GPU device, used for creating hardware resources for rendering/compute
RenderQueue:
The GPU queue for submitting work to the hardware
RenderAdapter:
Handle to the physical GPU hardware
RenderAdapterInfo:
Information about the GPU hardware that Bevy is running on

Input Handling Resources
These resources represent the current state of different input devices. Read them from your
systems to handle user input.

Input<KeyCode>:
Keyboard key state, as a binary Input value
Input<MouseButton>:
Mouse button state, as a binary Input value
Input<GamepadButton>:
Gamepad buttons, as a binary Input value
Axis<GamepadAxis>:
Analog Axis gamepad inputs (joysticks and triggers)
Axis<GamepadButton>:
Gamepad buttons, represented as an analog Axis value
Touches:
The state of all fingers currently touching the touchscreen
Gamepads:
Registry of all the connected Gamepad IDs

Events
(more info about working with events)
Input Events
These events fire on activity with input devices. Read them to [handle user input][cb::input].

MouseButtonInput:
Changes in the state of mouse buttons
MouseWheel:
Scrolling by a number of pixels or lines (MouseScrollUnit)
MouseMotion:
Relative movement of the mouse (pixels from previous frame), regardless of the OS pointer/cursor
CursorMoved:
New position of the OS mouse pointer/cursor
KeyboardInput:
Changes in the state of keyboard keys (keypresses, not text)
ReceivedCharacter:
Unicode text input from the OS (correct handling of the user's language and layout)
Ime:
Unicode text input from IME (support for advanced text input in different scripts)
TouchInput:
Change in the state of a finger touching the touchscreen
GamepadEvent:
Changes in the state of a gamepad or any of its buttons or axes
GamepadRumbleRequest:
Send these events to control gamepad rumble
TouchpadMagnify:
Pinch-to-zoom gesture on laptop touchpad (macOS)
TouchpadRotate:
Two-finger rotate gesture on laptop touchpad (macOS)

Engine Events
Events related to various internal things happening during the
normal runtime of a Bevy app.

AssetEvent<T>:
Sent by Bevy when asset data has been added/modified/removed; can be used to detect changes to assets
HierarchyEvent:
Sent by Bevy when entity parents/children change
AppExit:
Tell Bevy to shut down

System and Control Events
Events from the OS / windowing system, or to control Bevy.

RequestRedraw:
In an app that does not refresh continuously, request one more update before going to sleep
FileDragAndDrop:
The user drag-and-dropped a file into our app
CursorEntered:
OS mouse pointer/cursor entered one of our windows
CursorLeft:
OS mouse pointer/cursor exited one of our windows
WindowCloseRequested:
OS wants to close one of our windows
WindowCreated:
New application window opened
WindowClosed:
Bevy window closed
WindowDestroyed:
OS window freed/dropped after window close
WindowFocused:
One of our windows is now focused
WindowMoved:
OS/user moved one of our windows
WindowResized:
OS/user resized one of our windows
WindowScaleFactorChanged:
One of our windows has changed its DPI scaling factor
WindowBackendScaleFactorChanged:
OS reports change in DPI scaling factor for a window

Components
The complete list of individual component types is too specific to be useful to list here.
See: (List in API Docs)

### References
[[Input Handling  Unofficial Bevy Cheat Book]] [[Spatial Audio  Unofficial Bevy Cheat Book]] [[3D Models and Scenes GLTF  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[NonSend  Unofficial Bevy Cheat Book]] [[]] [[Systems  Unofficial Bevy Cheat Book]] [[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Local Resources  Unofficial Bevy Cheat Book]] [[]] [[States  Unofficial Bevy Cheat Book]] [[Render Stages  Unofficial Bevy Cheat Book]] [[Change Detection  Unofficial Bevy Cheat Book]] [[Visibility  Unofficial Bevy Cheat Book]] [[React to Changes with Asset Events  Unofficial Bevy Cheat Book]] [[ParamSet  Unofficial Bevy Cheat Book]] [[Customizing Bevy features modularity  Unofficial Bevy Cheat Book]] [[ParentChild Hierarchies  Unofficial Bevy Cheat Book]] [[]] [[3D Models and Scenes GLTF  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[]] [[Render Architecture Overview  Unofficial Bevy Cheat Book]] [[Asset Management  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[Custom Audio Streams  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] 