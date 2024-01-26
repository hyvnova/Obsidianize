Bevy Version:0.9(outdated!)


Change Detection
Relevant official examples:
component_change_detection.

Bevy allows you to easily detect when data is changed. You can use this to
perform actions in response to changes.
One of the main use cases is optimization – avoiding unnecessary work by
only doing it if the relevant data has changed. Another use case is triggering
special actions to occur on changes, like configuring something or sending
the data somewhere.
Components
Filtering
You can make a query that only yields entities if specific
components on them have been modified.
Use query filters:

Added<T>: detect new component instances

if the component was added to an existing entity
if a new entity with the component was spawned


Changed<T>: detect component instances that have been changed

triggers when the component is accessed mutably
also triggers if the component is newly-added (as per Added)



(If you want to react to removals, see the page on removal
detection. It works differently and is much
trickier to use.)
/// Print the stats of friendly players when they change
fn debug_stats_change(
    query: Query<
        // components
        (&Health, &PlayerXp),
        // filters
        (Without<Enemy>, Or<(Changed<Health>, Changed<PlayerXp>)>), 
    >,
) {
    for (health, xp) in query.iter() {
        eprintln!(
            "hp: {}+{}, xp: {}",
            health.hp, health.extra, xp.0
        );
    }
}

/// detect new enemies and print their health
fn debug_new_hostiles(
    query: Query<(Entity, &Health), Added<Enemy>>,
) {
    for (entity, health) in query.iter() {
        eprintln!("Entity {:?} is now an enemy! HP: {}", entity, health.hp);
    }
}
Checking
If you want to access all the entities, as normal, regardless of if they have
been modified, but you just want to check the status, you can use the special
ChangeTrackers<T> query parameter.
/// Make sprites flash red on frames when the Health changes
fn debug_damage(
    mut query: Query<(&mut Sprite, ChangeTrackers<Health>)>,
) {
    for (mut sprite, tracker) in query.iter_mut() {
        // detect if the Health changed this frame
        if tracker.is_changed() {
            sprite.color = Color::RED;
        } else {
            // extra check so we don't mutate on every frame without changes
            if sprite.color != Color::WHITE {
                sprite.color = Color::WHITE;
            }
        }
    }
}
This is useful for processing all entities, but doing different things
depending on if they have been modified.
Resources
For resources, change detection is provided via methods on the
Res/ResMut system parameters.
fn check_res_changed(
    my_res: Res<MyResource>,
) {
    if my_res.is_changed() {
        // do something
    }
}

fn check_res_added(
    // use Option, not to panic if the resource doesn't exist yet
    my_res: Option<Res<MyResource>>,
) {
    if let Some(my_res) = my_res {
        // the resource exists

        if my_res.is_added() {
            // it was just added
            // do something
        }
    }
}
Note that change detection cannot currently be used to detect
states changes (via the State
resource) (bug).
What gets detected?
Changed detection is triggered by
DerefMut. Simply accessing components via a mutable query,
without actually performing a &mut access, will not trigger it.
This makes change detection quite accurate. You can rely on it to optimize
your game's performance, or to otherwise trigger things to happen.
Also note that when you mutate a component, Bevy does not track if the new
value is actually different from the old value. It will always trigger the
change detection. If you want to avoid that, simply check it yourself:
fn update_player_xp(
    mut query: Query<&mut PlayerXp>,
) {
    for mut xp in query.iter_mut() {
        let new_xp = maybe_lvl_up(&xp);

        // avoid triggering change detection if the value is the same
        if new_xp != *xp {
            *xp = new_xp;
        }
    }
}
Change detection works on a per-system granularity, and is
reliable. A system will not detect changes that it made itself, only those
done by other systems, and only if it has not seen them before (the changes
happened since the last time it ran). If your system only runs sometimes
(such as with states or run criteria),
you do not have to worry about missing changes.
Possible Pitfalls
Beware of frame delay / 1-frame-lag. This can occur if Bevy runs the detecting
system before the changing system. The detecting system will see the change
the next time it runs, typically on the next frame update.
If you need to ensure that changes are handled immediately / during the same
frame, you can use explicit system ordering.
However, when detecting component additions with Added<T>
(which are typically done using Commands), this is not
enough; you need stages.
Removal Detection
Relevant official examples:
removal_detection.

Removal detection is special. This is because, unlike with change
detection, the data does not exist in the ECS anymore
(obviously), so Bevy cannot keep tracking metadata for it.
Nevertheless, being able to respond to removals is important for some
applications, so Bevy offers a limited form of it.
Components
You can check for components that have been removed during
the current frame. The data is cleared at the end of every frame update. Note
that this makes this feature tricky to use, and requires you to use multiple
stages.
When you remove a component (using Commands
(Commands)), the operation is applied at the end of the
stage. The system that checks for the removal
must run in a later stage during the same frame update. Otherwise, it will
not detect the removal.
Use the RemovedComponents<T> special system
parameter type, to get an iterator for the Entity IDs of
all the entities that had a component of type T that was removed earlier
this frame.
/// Some component type for the sake of this example.
#[derive(Component)]
struct Seen;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        // we could add our system to Bevy's `PreUpdate` stage
        // (alternatively, you could create your own stage)
        .add_system_to_stage(CoreStage::PreUpdate, remove_components)
        // our detection system runs in a later stage
        // (in this case: Bevy's default `Update` stage)
        .add_system(detect_removals)
        .run();
}

fn remove_components(
    mut commands: Commands,
    q: Query<(Entity, &Transform), With<Seen>>,
) {
    for (e, transform) in q.iter() {
        if transform.translation.y < -10.0 {
            // remove the `Seen` component from the entity
            commands.entity(e)
                .remove::<Seen>();
        }
    }
}

fn detect_removals(
    removals: RemovedComponents<Seen>,
    // ... (maybe Commands or a Query ?) ...
) {
    for entity in removals.iter() {
        // do something with the entity
    }
}
(To do things with these entities, you can just use the Entity IDs with
Commands::entity() or Query::get().)
Resources
Bevy does not provide any API for detecting when resources are removed.
You can work around this using Option and a separate
Local system parameter, effectively implementing your own
detection.
fn detect_removed_res(
    my_res: Option<Res<MyResource>>,
    mut my_res_existed: Local<bool>,
) {
    if let Some(my_res) = my_res {
        // the resource exists!

        // remember that!
        *my_res_existed = true;

        // (... you can do something with the resource here if you want ...)
    } else if *my_res_existed {
        // the resource does not exist, but we remember it existed!
        // (it was removed)

        // forget about it!
        *my_res_existed = false;

        // ... do something now that it is gone ...
    }
}
Note that, since this detection is local to your system, it does not have
to happen during the same frame update.

### References
[[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Local Resources  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Change Detection  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Change Detection  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 