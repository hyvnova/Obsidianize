Bevy Version:0.12(current)


2D Camera Setup
Cameras in Bevy are mandatory to see anything: they configure the
rendering.
This page will teach you about the specifics of 2D cameras. If you want to learn about
general non-2D specific functionality, see the general page on cameras.
Creating a 2D Camera
Bevy provides a bundle (Camera2dBundle)
that you can use to spawn a camera entity. It
has reasonable defaults to set up everything correctly.
You might want to set the transform, to position the camera.
#[derive(Component)]
struct MyCameraMarker;

fn setup_camera(mut commands: Commands) {
    commands.spawn((
        Camera2dBundle {
            transform: Transform::from_xyz(100.0, 200.0, 0.0),
            ..default()
        },
        MyCameraMarker,
    ));
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup_camera)
        .run();
}
Projection
The projection is what determines how coordinates map to the
viewport (commonly, the screen/window).
2D cameras always use an Orthographic projection.
When you spawn a 2D camera using Camera2dBundle,
it adds the OrthographicProjection
component to your entity. When
you are working with 2D cameras and you want to access
the projection, you should query for
OrthographicProjection.
fn debug_projection(
    query_camera: Query<&OrthographicProjection, With<MyCameraMarker>>,
) {
    let projection = query_camera.single();
    // ... do something with the projection
}
Note that this is different from 3D. If you are
making a library or some other code that should be able to handle both 2D and
3D, you cannot make a single query to access both 2D and 3D
cameras. You should create separate systems, or at least two
separate queries, to handle each kind of camera. This makes sense, as you will
likely need different logic for 2D vs. 3D anyway.
Caveat: near/far values
The projection contains the near and far values, which indicate the minimum
and maximum Z coordinate (depth) that can be rendered, relative to the position
(transform) of the camera.
Camera2dBundle sets them appropriately for 2D:
-1000.0 to 1000.0, allowing entities to be displayed on both positive and
negative Z coordinates. However, if you create the
OrthographicProjection yourself, to change any
other settings, you need to set these values yourself. The default value of the
OrthographicProjection struct is designed for
3D and has a near value of 0.0, which means you might not be able to see
your 2D entities.
commands.spawn((
    Camera2dBundle {
        projection: OrthographicProjection {
            // don't forget to set `near` and `far`
            near: -1000.0,
            far: 1000.0,
            // ... any other settings you want to change ...
            ..default()
        },
        ..default()
    },
    MyCameraMarker,
));
A more foolproof way to go about this is to use a temporary variable, to let the
bundle do its thing, and then mutate whatever you want. This way, you don't have
to worry about the exact values or getting anything wrong:
let mut camera_bundle = Camera2dBundle::default();
// change the settings we want to change:
camera_bundle.projection.scale = 2.0;
camera_bundle.transform.rotate_z(30f32.to_radians());
// ...

commands.spawn((
    camera_bundle,
    MyCameraMarker,
));
Scaling Mode
You can set the ScalingMode according to how you want to
handle window size / resolution.
The default for Bevy 2D cameras is to have 1 screen pixel correspond to 1 world
unit, thus allowing you to think of everything in "pixels". When the window is
resized, that causes more or less content to be seen.
If you want to keep this window resizing behavior, but change the mapping of screen
pixels to world units, use ScalingMode::WindowSize(x) with a value other than 1.0.
The value represents the number of screen pixels for one world unit.
If, instead, you want to always fit the same amount of content
on-screen, regardless of resolution, you should use something like
ScalingMode::FixedVertical or ScalingMode::AutoMax. Then, you can directly
specify how many units you want to display on-screen, and your content will
be upscaled/downscaled as appropriate to fit the window size.
use bevy::render::camera::ScalingMode;

let mut my_2d_camera_bundle = Camera2dBundle::default();
// For this example, let's make the screen/window height correspond to
// 1600.0 world units. The width will depend on the aspect ratio.
my_2d_camera_bundle.projection.scaling_mode = ScalingMode::FixedVertical(1600.0);
my_2d_camera_bundle.transform = Transform::from_xyz(100.0, 200.0, 0.0);

commands.spawn((
    my_2d_camera_bundle,
    MyCameraMarker,
));
Zooming
To "zoom" in 2D, you can change the orthographic projection's scale. This
allows you to just scale everything by some factor, regardless of the
ScalingMode behavior.
fn zoom_scale(
    mut query_camera: Query<&mut OrthographicProjection, With<MyCameraMarker>>,
) {
    let mut projection = query_camera.single_mut();
    // zoom in
    projection.scale /= 1.25;
    // zoom out
    projection.scale *= 1.25;
}
Alternatively, you can reconfigure the ScalingMode. This
way you can be confident about how exactly coordinates/units map to the
screen. This also helps avoid scaling artifacts with 2D assets, especially
pixel art.
fn zoom_scalingmode(
    mut query_camera: Query<&mut OrthographicProjection, With<MyCameraMarker>>,
) {
    use bevy::render::camera::ScalingMode;

    let mut projection = query_camera.single_mut();
    // 4 screen pixels to world/game pixel
    projection.scaling_mode = ScalingMode::WindowSize(4.0);
    // 6 screen pixels to world/game pixel
    projection.scaling_mode = ScalingMode::WindowSize(6.0);
}
Consider having a list of predefined "zoom levels" / scale values, so that you
can make sure your game always looks good.
If you are making a pixel-art game, you want to make sure the default texture
filtering mode is set to Nearest (and not Linear), if you want your pixels
to appear crisp instead of blurry:
fn main() {
    App::new()
        .add_plugins(
            DefaultPlugins
                .set(ImagePlugin::default_nearest())
        )
        // ...
        .run();
}
However, when downscaling, Linear (the default) filtering is preferred
for higher quality. So, for games with high-res assets, you want to leave
it unchanged.

### References
[[Cameras  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Cameras  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[3D Camera Setup  Unofficial Bevy Cheat Book]] [[Cameras  Unofficial Bevy Cheat Book]] 