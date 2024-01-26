Bevy Version:0.9(outdated!)


Touchscreen
Relevant official examples:
touch_input,
touch_input_events.

Multi-touch touchscreens are supported. You can track multiple fingers on
the screen, with position and pressure/force information. Bevy does not
offer gesture recognition.
The Touches resource allows you to track any
fingers currently on the screen:
fn touches(
    touches: Res<Touches>,
) {
    // There is a lot more information available, see the API docs.
    // This example only shows some very basic things.

    for finger in touches.iter() {
        if touches.just_pressed(finger.id()) {
            println!("A new touch with ID {} just began.", finger.id());
        }
        println!(
            "Finger {} is at position ({},{}), started from ({},{}).",
            finger.id(),
            finger.position().x,
            finger.position().y,
            finger.start_position().x,
            finger.start_position().y,
        );
    }
}
Alternatively, you can use TouchInput events:
fn touch_events(
    mut touch_evr: EventReader<TouchInput>,
) {
    use bevy::input::touch::TouchPhase;
    for ev in touch_evr.iter() {
        // in real apps you probably want to store and track touch ids somewhere
        match ev.phase {
            TouchPhase::Started => {
                println!("Touch {} started at: {:?}", ev.id, ev.position);
            }
            TouchPhase::Moved => {
                println!("Touch {} moved to: {:?}", ev.id, ev.position);
            }
            TouchPhase::Ended => {
                println!("Touch {} ended at: {:?}", ev.id, ev.position);
            }
            TouchPhase::Cancelled => {
                println!("Touch {} cancelled at: {:?}", ev.id, ev.position);
            }
        }
    }
}

### References
[[Events  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 