Bevy Version:0.12(current)


Setting the Window Icon
You might want to set a custom Window Icon. On Windows and Linux, this is
the icon image shown in the window title bar (if any) and task bar (if any).
Unfortunately, Bevy does not yet provide an easy and ergonomic built-in way
to do this. However, it can be done via the winit APIs.
The way shown here is quite hacky. To save on code complexity, instead of
using Bevy's asset system to load the image in the background, we bypass
the assets system and directly load the file using the image library.
There is some WIP on adding a proper API for this to Bevy; see PRs
#1163, #2268, #5488,
#8130, and Issue #1031.
This example shows how to set the icon for the primary/main window, from
a Bevy startup system.
use bevy::winit::WinitWindows;
use winit::window::Icon;

fn set_window_icon(
    // we have to use `NonSend` here
    windows: NonSend<WinitWindows>,
) {
    // here we use the `image` crate to load our icon data from a png file
    // this is not a very bevy-native solution, but it will do
    let (icon_rgba, icon_width, icon_height) = {
        let image = image::open("my_icon.png")
            .expect("Failed to open icon path")
            .into_rgba8();
        let (width, height) = image.dimensions();
        let rgba = image.into_raw();
        (rgba, width, height)
    };
    let icon = Icon::from_rgba(icon_rgba, icon_width, icon_height).unwrap();

    // do it for all windows
    for window in windows.windows.values() {
        window.set_window_icon(Some(icon.clone()));
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, set_window_icon)
        .run();
}
Note: that WinitWindows is a non-send
resource.
Note: you need to add winit to your project's dependencies, and it must
be the same version as the one used by Bevy. You can use cargo tree or
check Cargo.lock to see which is the correct version. As of Bevy 0.12,
that should be winit = "0.28". You should also try to match the version
of the image library; Bevy uses image = "0.24".

### References
[[NonSend  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 