# Code-smell baseline

Adapted from mattpocock/skills `code-review`, after Martin Fowler, *Refactoring*, chapter 3. The Standards axis always carries this list, even when the repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo rule always wins; where the repo endorses something below, do not flag it.
- **Always a judgement call.** Report each as "possible <smell>", never as a hard violation. Skip anything a linter or formatter already enforces.

Each line: what it is → usual fix.

- **Mysterious Name:** a name that does not say what the thing does or holds → rename; if no honest name comes, the design is unclear.
- **Duplicated Code:** the same logic shape in more than one hunk or file of the change → extract it and call it from both.
- **Feature Envy:** a function that uses another object's data more than its own → move it next to that data.
- **Data Clumps:** the same few fields or parameters always travel together → make them one type.
- **Primitive Obsession:** a primitive or string standing in for a domain concept → give the concept its own small type.
- **Repeated Switches:** the same switch or if-cascade on the same type in several places → polymorphism, or one shared map.
- **Shotgun Surgery:** one logical change forces scattered edits across many files → gather what changes together.
- **Divergent Change:** one module edited for several unrelated reasons → split it so each part changes for one reason.
- **Speculative Generality:** hooks, parameters, or abstractions for needs the spec does not have → remove until a real need appears.
- **Message Chains:** long `a.b().c().d()` walks the caller should not depend on → hide the walk behind one call.
- **Middle Man:** a unit that mostly delegates → call the real target directly.
- **Refused Bequest:** a subtype that ignores or overrides most of what it inherits → use composition.
