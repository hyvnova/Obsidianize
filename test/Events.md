Bevy Version:0.11(outdated!)


Events
Relevant official examples:
event.

Send data between systems! Let your systems communicate with each other!
Like resources or components, events are
simple Rust structs or enums. When creating a new event type, derive
the Event trait.
Then, any system can send (broadcast) values of that type,
and any system can receive those events.

To send events, use an EventWriter<T>.
To receive events, use an EventReader<T>.

Every reader tracks the events it has read independently, so you can handle
the same events from multiple systems.
#[derive(Event)]
struct LevelUpEvent(Entity);

fn player_level_up(
    mut ev_levelup: EventWriter<LevelUpEvent>,
    query: Query<(Entity, &PlayerXp)>,
) {
    for (entity, xp) in query.iter() {
        if xp.0 > 1000 {
            ev_levelup.send(LevelUpEvent(entity));
        }
    }
}

fn debug_levelups(
    mut ev_levelup: EventReader<LevelUpEvent>,
) {
    for ev in ev_levelup.iter() {
        eprintln!("Entity {:?} leveled up!", ev.0);
    }
}
You need to register your custom event types via the app builder:
app.add_event::<LevelUpEvent>();
Usage Advice
Events should be your go-to data flow tool. As events can be sent from any
system and received by multiple systems, they are extremely
versatile.
Events can be a very useful layer of abstraction. They allow you to decouple
things, so you can separate different functionality and more easily reason
about which system is responsible for what.
You can imagine how, even in the simple "player level up" example shown above,
using events would allow us to easily extend our hypothetical game with more
functionality. If we wanted to display a fancy level-up effect or animation,
update UI, or anything else, we can just add more systems that read the events
and do their respective things. If the player_level_up system had simply
checked the player XP and managed the player level directly, without going via
events, it would be unwieldy for future development of the game.
How it all works
When you register an event type, Bevy will create an Events<T>
resource, which acts as the backing storage for the event queue. Bevy
also adds an "event maintenance" system to clear events every
frame, preventing them from accumulating and using up memory.
The events storage is double-buffered, meaning that events stay for one extra
frame after the frame when they were sent. This gives your systems a chance to
read the events on the next frame, if they did not get a chance during the
current frame.
If you don't like this, you can have manual control over when events are
cleared (at the risk of leaking / wasting memory if you
forget to clear them).
The EventWriter<T> system parameter is just syntax sugar
for mutably accessing the Events<T> resource to
add events to the queue. The EventReader<T> is a little
more complex: it accesses the events storage immutably, but also stores an
integer counter to keep track of how many events you have read. This is why it
also needs the mut keyword.
Possible Pitfalls
Beware of frame delay / 1-frame-lag. This can occur if Bevy runs the receiving
system before the sending system. The receiving system will only get a chance
to receive the events on the next frame update. If you need to ensure that
events are handled immediately / during the same frame, you can use explicit
system ordering.
Beware of lost events if you do not read events every frame, or at least once
every other frame update. A common situation where this can occur is when
using a fixed timestep or run conditions.
If you want events to persist for longer than two frames, you can implement a
custom cleanup/management strategy. However, you can only do
this for your own event types. There is no solution for Bevy's
built-in types.

### References
[[Manual Event Clearing  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 