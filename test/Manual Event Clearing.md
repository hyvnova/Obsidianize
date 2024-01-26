Bevy Version:0.9(outdated!)


Manual Event Clearing
The event queue needs to be cleared periodically,
so that it does not grow indefinitely and waste unbounded memory.
Bevy's default cleanup strategy is to clear events every frame, but with double
buffering, so that events from the previous frame update stay available. This
means that you can handle the events only until the end of the next frame
after the one when they are sent.
This default works well for systems that run every frame and check for events
every time, which is the typical usage pattern.
However, if you have systems that do not read events every frame, they might
miss some events. Some common scenarios where this occurs are:

systems with an early-return, that don't read events every time they run
when using fixed timestep
systems that only run in specific states,
such as if your game has a pause state
when using custom run criteria to control
your systems

To be able to reliably manage events in such circumstances, you might want
to have manual control over how long the events are held in memory.
You can replace Bevy's default cleanup strategy with your own.
To do this, simply add your event type (wrapped as Events<T>)
to the app builder using .init_resource, instead of .add_event.
(.add_event is actually just a convenience method that initializes the
resource and adds Bevy's built-in system (generic
over your event type) for the default cleanup strategy)
You must then clear the events at your discretion. If you don't do this often
enough, your events might pile up and waste memory.
Example
We can create generic systems for this. Implement
the custom cleanup strategy, and then add that system to your
App as many times as you need, for each event type
where you want to use your custom behavior.
use bevy::ecs::event::Events;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // add the `Events<T>` resource manually
        // these events will not have automatic cleanup
        .init_resource::<Events<MySpecialEvent>>()

        // this is a regular event type with automatic cleanup
        .add_event::<MyRegularEvent>()

        // add the cleanup systems
        .add_system(my_event_manager::<MySpecialEvent>)
        .run();
}

/// Custom cleanup strategy for events
///
/// Generic to allow using for any custom event type
fn my_event_manager<T: 'static + Send + Sync>(
    mut events: ResMut<Events<T>>,
) {
    // TODO: implement your custom logic
    // for deciding when to clear the events

    // clear all events like this:
    events.clear();

    // or with double-buffering
    // (this is what Bevy's default strategy does)
    events.update();

    // or drain them, if you want to iterate,
    // to access the values:
    for event in events.drain() {
        // TODO: do something with each event
    }
}

### References
[[Introduction  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Generic Systems  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 