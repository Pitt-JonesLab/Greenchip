The marker script operates on a line-by-line basis. Each line is read as a marker command, and should be structured in the following way

MarkerSpecifier Sleep Activity Radius Label Color

MarkerSpecifier - This should be either "M" or "WM" (not case sensitive.) "M" specifies a regular marker, and "WM" specifies a wide marker.

Sleep - This should be a number that specifies the marker's sleep ratio (should be between 0 and 100)

Activity - This should be a number that specifies the marker's activity ratio (should be between 0 and 100)

Radius - This is a number tat is only used in the "WM" mode to specify the marker's radius. If you are in the "M" mode, don't put anything here (don't put an extra space either)

Label - This specifies the marker's label

Color(optional) - This specifies the marker's color (not case sensitive). It ports the string directly to matplotlib, so check matplotlib's color list to see which one you want to use. If nothing is specified here, then the label will be black with a white bounding box

Some examples are given below:

M 20 40 Phone2 red: This creates a marker with sleep ratio of 20, activity ratio of 40, and a red label of Phone2.

WM 30 60 15 Tablet: This creates a wide marker with sleep ratio of 30, activity ratio of 60, a radius of 15, and a label of Tablet. It uses the default label color scheme of black with a white bounding box


M 30 10 Laptop: This creates a marker with sleep ratio of 30, activity ratio of 10, and a label of Laptop. It again uses the default label color scheme.