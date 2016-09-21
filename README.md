Shoot tennis balls at targets.

Detect equilateral triangular targets using a Raspberry Pi and a camera.
1. Find all pixels within tolerance of a particular color
2. Apply thinning algorithm to found pixels
3. Apply Hough transform
4. Find all points of intersection of lines from Hough transform
5. Find all sets of points that make equilateral triangles of reasonable size; these (hopefully) are the targets

Two Raspberry Pis are used, each connected to a separate camera. The cameras are arranged in a vertical line. After both Pis finish detecting targets, they communicate their results to each other. The device can be rotated to aim at any desired target. Distance to each target is calculated using the difference in y position between the detected targets from each camera. After the device is aimed and distance is calculated, the wheel is spun to a desired RPM (using empirical data) depending on distance to and height of target, and the ball is shot.
