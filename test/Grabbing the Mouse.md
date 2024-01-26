Bevy Version:0.12(current)


Grabbing the Mouse
Relevant official examples:
mouse_grab.

For some genres of games, you want to the mouse to be restricted to the window,
to prevent it from leaving the window during gameplay.
To grab the cursor:
use bevy::window::{CursorGrabMode, PrimaryWindow};

fn cursor_grab(
    mut q_windows: Query<&mut Window, With<PrimaryWindow>>,
) {
    let mut primary_window = q_windows.single_mut();

    // if you want to use the cursor, but not let it leave the window,
    // use `Confined` mode:
    primary_window.cursor.grab_mode = CursorGrabMode::Confined;

    // for a game that doesn't use the cursor (like a shooter):
    // use `Locked` mode to keep the cursor in one place
    primary_window.cursor.grab_mode = CursorGrabMode::Locked;

    // also hide the cursor
    primary_window.cursor.visible = false;
}
To release the cursor:
fn cursor_ungrab(
    mut q_windows: Query<&mut Window, With<PrimaryWindow>>,
) {
    let mut primary_window = q_windows.single_mut();

    primary_window.cursor.grab_mode = CursorGrabMode::None;
    primary_window.cursor.visible = true;
}
You should grab the cursor during active gameplay and release it when
the player pauses the game / exits to menu / etc.
For relative mouse movement, you should use mouse motion
instead of cursor input to implement your gameplay.
Platform Differences
macOS does not natively support Confined mode. Bevy will fallback to Locked.
If you want to support macOS and you want to use cursor input,
you might want to implement a "virtual cursor" instead.
Windows does not natively support Locked mode. Bevy will fallback to Confined.
You could emulate the locked behavior by re-centering the cursor every frame:
#[cfg(target_os = "windows")]
fn cursor_recenter(
    mut q_windows: Query<&mut Window, With<PrimaryWindow>>,
) {
    let mut primary_window = q_windows.single_mut();
    let center = Vec2::new(
        primary_window.width() / 2.0,
        primary_window.height() / 2.0,
    );
    primary_window.set_cursor_position(Some(center));
}
#[cfg(target_os = "windows")]
app.add_systems(Update, cursor_recenter);

### References
[[Mouse  Unofficial Bevy Cheat Book]] [[Mouse  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 