Bevy Version:0.12(current)


Cameras
Cameras drive all rendering in Bevy. They are responsible for configuring what
to draw, how to draw it, and where to draw it.
You must have at least one camera entity, in order for anything to be displayed
at all! If you forget to spawn a camera, you will get an empty black screen.
In the simplest case, you can create a camera with the default settings. Just
spawn an entity using Camera2dBundle or
Camera3dBundle. It will simply draw all renderable
entities that are visible.
This page gives a general overview of cameras in Bevy. Also see the dedicated
pages for 2D cameras and 3D cameras.
Practical advice: always create marker components for
your camera entities, so that you can query your cameras easily!
#[derive(Component)]
struct MyGameCamera;

fn setup(mut commands: Commands) {
    commands.spawn((
        Camera3dBundle::default(),
        MyGameCamera,
    ));
}
The Camera Transform
Cameras have transforms, which can be used to position or
rotate the camera. This is how you move the camera around.
For examples, see these cookbook pages:

3D pan-orbit camera, like in 3D editor apps

If you are making a game, you should implement your own custom camera controls
that feel appropriate to your game's genre and gameplay.
Zooming the camera
Do not use the transform scale to "zoom" a camera! It just stretches the image,
which is not "zooming". It might also cause other issues and incompatibilities.
Use the projection to zoom.
For an orthographic projection, change the scale. For a perspective projection,
change the FOV. The FOV mimics the effect of zooming with a lens.
Learn more about how to do this in 2D or
3D.
Projection
The camera projection is responsible for mapping the coordinate system to the
viewport (commonly, the screen/window). It is what configures the coordinate
space, as well as any scaling/stretching of the image.
Bevy provides two kinds of projections:
OrthographicProjection and
PerspectiveProjection. They are configurable,
to be able to serve a variety of different use cases.
Orthographic means that everything always appears the same size, regardless of
how far away it is from the camera.
Perspective means that things appear smaller the further away they are from
the camera. This is the effect that gives 3D graphics a sense of depth and
distance.
2D cameras are always orthographic.
3D cameras can use either kind of projection. Perspective is
the most common (and default) choice. Orthographic is useful for applications
such as CAD and engineering, where you want to accurately represent the
dimensions of an object, instead of creating a realistic sense of 3D space. Some
games (notably simulation games) use orthographic as an artistic choice.
It is possible to implement your own custom camera
projections. This can give you full control over
the coordinate system. However, beware that things might behave in unexpected
ways if you violate Bevy's coordinate system conventions!
HDR and Tonemapping
See here!
Render Target
The render target of a camera determines where the GPU will draw things to. It
could be a window (for outputting directly to the screen) or an
Image asset (render-to-texture).
By default, cameras output to the primary window.
use bevy::render::camera::RenderTarget;

fn debug_render_targets(
    q: Query<&Camera>,
) {
    for camera in &q {
        match &camera.target {
            RenderTarget::Window(wid) => {
                eprintln!("Camera renders to window with id: {:?}", wid);
            }
            RenderTarget::Image(handle) => {
                eprintln!("Camera renders to image asset with id: {:?}", handle);
            }
            RenderTarget::TextureView(_) => {
                eprintln!("This is a special camera that outputs to something outside of Bevy.");
            }
        }
    }
}
Viewport
The viewport is an (optional) way to restrict a camera to a sub-area of its
render target, defined as a rectangle. That rectangle is effectively treated as
the "window" to draw in.
An obvious use-case are split-screen games, where you want a camera to only draw
to one half of the screen.
use bevy::render::camera::Viewport;

fn setup_minimap(mut commands: Commands) {
    commands.spawn((
        Camera2dBundle {
            camera: Camera {
                // renders after / on top of other cameras
                order: 2,
                // set the viewport to a 256x256 square in the top left corner
                viewport: Some(Viewport {
                    physical_position: UVec2::new(0, 0),
                    physical_size: UVec2::new(256, 256),
                    ..default()
                }),
                ..default()
            },
            ..default()
        },
        MyMinimapCamera,
    ));
}
If you need to find out the area a camera renders to (the viewport, if
configured, or the entire window, if not):
fn debug_viewports(
    q: Query<&Camera, With<MyExtraCamera>>,
) {
    let camera = q.single();

    // the size of the area being rendered to
    let view_dimensions = camera.logical_viewport_size().unwrap();

    // the coordinates of the rectangle covered by the viewport
    let rect = camera.logical_viewport_rect().unwrap();
}
Coordinate Conversion
Camera provides methods to help with coordinate conversion
between on-screen coordinates and world-space coordinates. For an example, see
the "cursor to world" cookbook page.
Clear Color
This is the "background color" that the whole viewport will be cleared to,
before a camera renders anything.
You can also disable clearing on a camera, if you want to preserve all the
pixels as they were before.
See this page for more info.
Render Layers
RenderLayers is a way to filter what entities should be
drawn by what cameras. Insert this component onto your entities
to place them in specific "layers". The layers are integers from 0 to 31 (32
total available).
Inserting this component onto a camera entity selects what layers that camera
should render. Inserting this component onto renderable entities selects what
cameras should render those entities. An entity will be rendered if there is any
overlap between the camera's layers and the entity's layers (they have at least
one layer in common).
If an entity does not have the RenderLayers component,
it is assumed to belong to layer 0 (only).
use bevy::render::view::visibility::RenderLayers;
// This camera renders everything in layers 0, 1
commands.spawn((
    Camera2dBundle::default(),
    RenderLayers::from_layers(&[0, 1])
));
// This camera renders everything in layers 1, 2
commands.spawn((
    Camera2dBundle::default(),
    RenderLayers::from_layers(&[1, 2])
));
// This sprite will only be seen by the first camera
commands.spawn((
    SpriteBundle::default(),
    RenderLayers::layer(0),
));
// This sprite will be seen by both cameras
commands.spawn((
    SpriteBundle::default(),
    RenderLayers::layer(1),
));
// This sprite will only be seen by the second camera
commands.spawn((
    SpriteBundle::default(),
    RenderLayers::layer(2),
));
// This sprite will also be seen by both cameras
commands.spawn((
    SpriteBundle::default(),
    RenderLayers::from_layers(&[0, 2]),
));
You can also modify the render layers of entities after they are spawned.
Camera Ordering
A camera's order is a simple integer value that controls the order relative
to any other cameras with the same render target.
For example, if you have multiple cameras that all render to the primary window,
they will behave as multiple "layers". Cameras with a higher order value will render
"on top of" cameras with a lower value. 0 is the default.
use bevy::core_pipeline::clear_color::ClearColorConfig;

commands.spawn((
    Camera2dBundle {
        camera_2d: Camera2d {
            // no "background color", we need to see the main camera's output
            clear_color: ClearColorConfig::None,
            ..default()
        },
        camera: Camera {
            // renders after / on top of the main camera
            order: 1,
            ..default()
        },
        ..default()
    },
    MyOverlayCamera,
));
UI Rendering
Bevy UI rendering is integrated into the cameras! Every camera will, by default,
also draw UI.
However, if you are working with multiple cameras, you probably only want your
UI to be drawn once (probably by the main camera). You can disable UI rendering
on your other cameras.
Also, UI on multiple cameras is currently broken in Bevy. Even if you want
multiple UI cameras (say, to display UI in an app with multiple windows), it
does not work correctly.
commands.spawn((
    Camera3dBundle::default(),
    // UI config is a separate component
    UiCameraConfig {
        show_ui: false,
    },
    MyExtraCamera,
));
Disabling Cameras
You can deactivate a camera without despawning it. This is useful when you want
to preserve the camera entity and all the configuration it carries, so you can
easily re-enable it later.
Some example use cases: toggling an overlay, switching between a 2D and 3D view.
fn toggle_overlay(
    mut q: Query<&mut Camera, With<MyOverlayCamera>>,
) {
    let mut camera = q.single_mut();
    camera.is_active = !camera.is_active;
}
Multiple Cameras
This is an overview of different scenarios where you would need more than one
camera entity.
Multiple Windows
Official example: multiple_windows.
If you want to create a Bevy app with multiple windows, you need to spawn
multiple cameras, one for each window, and set their render targets
respectively. Then, you can use your cameras to control what to display in each
window.
Split-Screen
Official example: split_screen.
You can set the camera viewport to only render to a part of the
render target. This way, a camera can be made to render one half of the screen
(or any other area). Use a separate camera for each view in a split-screen game.
Overlays
Official example: two_passes.
You might want to render multiple "layers" (passes) to the same render target.
An example of this might be an overlay/HUD to be displayed on top of the
main game.
The overlay camera could be completely different from the main camera. For
example, the main camera might draw a 3D scene, and the overlay camera might
draw 2D shapes. Such use cases are possible!
Use a separate camera to create the overlay. Set the priority
higher, to tell Bevy to render it after (on top of) the main camera. Make sure
to disable clearing!
Think about which camera you want to be responsible for rendering the
UI. Use the overlay camera if you want it to be unaffected,
or use the main camera if you want the overlay to be on top of the UI. Disable
it on the other camera.
Use Render Layers to control what entities should be rendered
by each camera.
Render to Image
(aka Render to Texture)
Official example: render_to_texture.
If you want to generate an image in memory, you can output to an Image asset.
This is useful for intermediate steps in games, such as rendering a minimap or
the gun in a shooter game. You can then use that image as part of the final
scene to render to the screen. Item previews are a similar use case.
Another use case is window-less applications that want to generate image files.
For example, you could use Bevy to render something, and then export it to a PNG
file.

### References
[[Asset Management  Unofficial Bevy Cheat Book]] [[Cameras  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Change the Background Color  Unofficial Bevy Cheat Book]] [[3D Camera Setup  Unofficial Bevy Cheat Book]] [[HDR and Tonemapping  Unofficial Bevy Cheat Book]] [[Convert cursor to world coordinates  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[3D Camera Setup  Unofficial Bevy Cheat Book]] [[Bevy Cookbook  Unofficial Bevy Cheat Book]] [[3D PanOrbit Camera  Unofficial Bevy Cheat Book]] [[Custom Camera Projection  Unofficial Bevy Cheat Book]] [[Visibility  Unofficial Bevy Cheat Book]] [[2D Camera Setup  Unofficial Bevy Cheat Book]] [[2D Camera Setup  Unofficial Bevy Cheat Book]] [[Coordinate System  Unofficial Bevy Cheat Book]] 