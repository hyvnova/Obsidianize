Bevy Version:0.11(outdated!)


Mouse
Relevant official examples:
mouse_input,
mouse_input_events.

Mouse Buttons
Similar to keyboard input, mouse buttons are available as an
Input state resource, events, and run
conditions (see list). Use whichever
pattern feels most appropriate to your use case.
You can check the state of specific mouse buttons using
Input<MouseButton>:
fn mouse_button_input(
    buttons: Res<Input<MouseButton>>,
) {
    if buttons.just_pressed(MouseButton::Left) {
        // Left button was pressed
    }
    if buttons.just_released(MouseButton::Left) {
        // Left Button was released
    }
    if buttons.pressed(MouseButton::Right) {
        // Right Button is being held down
    }
    // we can check multiple at once with `.any_*`
    if buttons.any_just_pressed([MouseButton::Left, MouseButton::Right]) {
        // Either the left or the right button was just pressed
    }
}
You can also iterate over any buttons that have been pressed or released:
fn mouse_button_iter(
    buttons: Res<Input<MouseButton>>,
) {
    for button in buttons.get_pressed() {
        println!("{:?} is currently held down", button);
    }
    for button in buttons.get_just_pressed() {
        println!("{:?} was pressed", button);
    }
    for button in buttons.get_just_released() {
        println!("{:?} was released", button);
    }
}
Alternatively, you can use MouseButtonInput
events to get all activity:
use bevy::input::mouse::MouseButtonInput;

fn mouse_button_events(
    mut mousebtn_evr: EventReader<MouseButtonInput>,
) {
    use bevy::input::ButtonState;

    for ev in mousebtn_evr.iter() {
        match ev.state {
            ButtonState::Pressed => {
                println!("Mouse button press: {:?}", ev.button);
            }
            ButtonState::Released => {
                println!("Mouse button release: {:?}", ev.button);
            }
        }
    }
}
You can also use Bevy's built-in run conditions, so your
systems only run on mouse button input. Only recommended for
prototyping; for proper projects you might want to implement your own run
conditions, to support rebinding or other custom use cases.
use bevy::input::common_conditions::*;

app.add_systems(Update, (
    handle_middleclick
        .run_if(input_just_pressed(MouseButton::Middle)),
    handle_drag
        .run_if(input_pressed(MouseButton::Left)),
));
Mouse Scrolling / Wheel
To detect scrolling input, use MouseWheel events:
use bevy::input::mouse::MouseWheel;

fn scroll_events(
    mut scroll_evr: EventReader<MouseWheel>,
) {
    use bevy::input::mouse::MouseScrollUnit;
    for ev in scroll_evr.iter() {
        match ev.unit {
            MouseScrollUnit::Line => {
                println!("Scroll (line units): vertical: {}, horizontal: {}", ev.y, ev.x);
            }
            MouseScrollUnit::Pixel => {
                println!("Scroll (pixel units): vertical: {}, horizontal: {}", ev.y, ev.x);
            }
        }
    }
}
The MouseScrollUnit enum is important: it tells
you the type of scroll input. Line is for hardware with fixed steps, like
the wheel on desktop mice. Pixel is for hardware with smooth (fine-grained)
scrolling, like laptop touchpads.
You should probably handle each of these differently (with different
sensitivity settings), to provide a good experience on both types of hardware.
Note: the Line unit is not guaranteed to have whole number values/steps!
At least macOS does non-linear scaling / acceleration of
scrolling at the OS level, meaning your app will get weird values for the number
of lines, even when using a regular PC mouse with a fixed-stepping scroll wheel.
Mouse Motion
Use this if you don't care about the exact position of the mouse cursor,
but rather you just want to see how much it moved from frame to frame. This
is useful for things like controlling a 3D camera.
Use MouseMotion events. Whenever the
mouse is moved, you will get an event with the delta.
use bevy::input::mouse::MouseMotion;

fn mouse_motion(
    mut motion_evr: EventReader<MouseMotion>,
) {
    for ev in motion_evr.iter() {
        println!("Mouse moved: X: {} px, Y: {} px", ev.delta.x, ev.delta.y);
    }
}
You might want to grab/lock the mouse inside the game
window.
Mouse Cursor Position
Use this if you want to accurately track the position pointer / cursor. This is
useful for things like clicking and hovering over objects in your game or UI.
You can get the current coordinates of the mouse pointer, from the respective
Window (if the mouse is currently inside that window):
use bevy::window::PrimaryWindow;

fn cursor_position(
    q_windows: Query<&Window, With<PrimaryWindow>>,
) {
    // Games typically only have one window (the primary window)
    if let Some(position) = q_windows.single().cursor_position() {
        println!("Cursor is inside the primary window, at {:?}", position);
    } else {
        println!("Cursor is not in the game window.");
    }
}
To detect when the pointer is moved, use CursorMoved
events to get the updated coordinates:
fn cursor_events(
    mut cursor_evr: EventReader<CursorMoved>,
) {
    for ev in cursor_evr.iter() {
        println!(
            "New cursor position: X: {}, Y: {}, in Window ID: {:?}",
            ev.position.x, ev.position.y, ev.window
        );
    }
}
Note that you can only get the position of the mouse inside a window;
you cannot get the global position of the mouse in the whole OS Desktop /
on the screen as a whole.
The coordinates you get are in "window space". They represent window
pixels, and the origin is the bottom left corner of the window. They do not
relate to your camera or in-game coordinates in any way. See this cookbook
example for converting these window cursor coordinates
into world-space coordinates.
To track when the mouse cursor enters and leaves your window(s), use
CursorEntered and CursorLeft
events.
Touchpad Gestures
Bevy supports the two-finger rotate and pinch-to-zoom gestures, but they
currently only work on macOS, where the OS provides special events for them.
If you are interested in supporting these gestures in your app, you can do so
using TouchpadRotate and
TouchpadMagnify events:
use bevy::input::touchpad::{TouchpadMagnify, TouchpadRotate};

// these only work on macOS
fn touchpad_gestures(
    mut evr_touchpad_magnify: EventReader<TouchpadMagnify>,
    mut evr_touchpad_rotate: EventReader<TouchpadRotate>,
) {
    for ev_magnify in evr_touchpad_magnify.iter() {
        // Positive numbers are zooming in
        // Negative numbers are zooming out
        println!("Touchpad zoom by {}", ev_magnify.0);
    }
    for ev_rotate in evr_touchpad_rotate.iter() {
        // Positive numbers are anticlockwise
        // Negative numbers are clockwise
        println!("Touchpad rotate by {}", ev_rotate.0);
    }
}

### References
[[Convert cursor to world coordinates  Unofficial Bevy Cheat Book]] [[Keyboard  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Input Handling  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[macOS Desktop  Unofficial Bevy Cheat Book]] [[GrabCapture the Mouse Cursor  Unofficial Bevy Cheat Book]] 