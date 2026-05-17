# Plotting tooling decision

## Verified references
- Matplotlib documentation states `matplotlib.pyplot` is a collection of functions that makes Matplotlib work like MATLAB.
- MATLAB documentation provides standard scientific plotting APIs (`plot`, `loglog`, etc.) widely used in technical courses.

## Decision for this repository
- Default for report-grade figures: Python + Matplotlib (reproducible, scriptable, standard in scientific Python).
- MATLAB/Octave is allowed if explicitly required by course instructions.
- Go plotting is optional and used only if resulting figure quality matches report requirements.
