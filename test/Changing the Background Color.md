Bevy Version:0.9(outdated!)


Changing the Background Color
Relevant official examples:
clear_color.

Use the ClearColor resource to choose the
default background color. This color will be used as the default for all
cameras, unless overriden.
Note that the window will be black if no cameras exist. You must spawn at
least one camera.
fn setup(
    mut commands: Commands,
) {
    commands.spawn(Camera2dBundle::default());
}

fn main() {
    App::new()
        // set the global default
        .insert_resource(ClearColor(Color::rgb(0.9, 0.3, 0.6)))
        .add_plugins(DefaultPlugins)
        .add_startup_system(setup)
        .run();
}
To override the default and use a different color for a specific
camera, you can set it using the Camera2d or
Camera3d components.
use bevy::core_pipeline::clear_color::ClearColorConfig;

// configure the background color (if any), for a specific camera (3D)
commands.spawn(Camera3dBundle {
    camera_3d: Camera3d {
        // clear the whole viewport with the given color
        clear_color: ClearColorConfig::Custom(Color::rgb(0.8, 0.4, 0.2)),
        ..Default::default()
    },
    ..Default::default()
});

// configure the background color (if any), for a specific camera (2D)
commands.spawn(Camera2dBundle {
    camera_2d: Camera2d {
        // disable clearing completely (pixels stay as they are)
        // (preserves output from previous frame or camera/pass)
        clear_color: ClearColorConfig::None,
    },
    ..Default::default()
});
All of these locations (the components on specific cameras, the global
default resource) can be mutated at runtime, and bevy will use your new color.
Changing the default color using the resource will apply the new color to all
existing cameras that do not specify a custom color, not just newly-spawned
cameras.

### References
[[Resources  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Cameras  Unofficial Bevy Cheat Book]] 