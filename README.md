# Paper transformations

When a piece of paper is photographed at a weird angle, it becomes difficult for both humans and OCR programs to read the text on it. Given an image containing an A series piece of paper, possibly at a very awkward angle, the code in this repository identifies the paper in the image and then simulates what it would look like if one were to look at the paper from directly above it.


## How to run
To be able to run the program, you need Python with NumPy, Matplotlib and OpenCV. 

The main script is located in *src/main.py*. When you run it you can specify the path to an image containing a piece of paper, and the program will process it and show you a window like the one below. On the left is the image you chose, with the paper corners marked with green dots, and on the right is what the paper looks like from directly above. If the program is unable to find a paper in the image, it will tell you that.

<img src="example_usecase.png" width="640" alt="Example usecase">


## How it works

The program works in two steps. In the first step we locate the paper and its corners in the image. In the second step we use the knowledge about the corner positions to find out which points of the paper in 3D correspond to which points in the image so that we can color the image to be displayed accordingly.

This repository includes two different ways to perform the second step. The old version is probably more "orthodox", hence why it was the first method I thought of using. The new version is much stranger, and I have never seen anything like it anywhere. I only came up with it after the whole project was "done" and still using the old version of step 2. The main method uses this new version because it is much less sensitive to when the program thinks the corners are at slightly different positions than they really are.

### Identifying the paper
First, a highpass filter, dilation and erosion are used to find edges and separate different regions in the image. We use Otsu's binarization to determine which of the regions are bright (if a region is not bright then it is guaranteed not to be the paper we are looking for). Then we go through all the bright regions and see if their convex hull can be approximated by a quadrilateral. To see if a convex hull is close to being a quadrilateral, we find the 4 points of the hull which create a quadrilateral of maximal area. If this area is close to the area of the convex hull, then we pretty much by definition have determined that the convex hull is close to being a quadrilateral. And if this is the case for a bright region, then the quadrilateral is deemed to be the paper.

### Perspective correction, new version

We use a pretty strange but interesting trick involving [vanishing points](https://en.wikipedia.org/wiki/Vanishing_point) to map arbitrarily many 3D points in the real paper to their projection in the camera image.

To start with, there are some important observations to be made about how the projection into the camera actually works:

1. If you take a photo of a line, then the midpoint of that line will in general not land on the midpoint of the line in the image. Intuitively speaking, this is because the part of the line that is closer to the camera will appear bigger in the image compared to the part that is further away, so the closest half will take up more than half of the line in the image. 
2. Not accounting for lens distortions, taking a photo of a straight line will always result in a straight line in the image. 

The first step is to find the center of the paper. According to point 1, we can't just take the averages of the corner points or something like that. However, with the help of point 2 we can draw the diagonals of the paper in the image (green lines in the image below), and their intersection will be in the center of the paper. We call the center C.

Next we need to find the midpoints of the sides. Extend the lines (blue lines in the image below) from two opposing sides of the paper in the image to find their vanishing point, call this point V. Now we draw a line (orange) from V, through C and extending it towards the bottom side of the paper. Since this line goes through both the center of the paper and the vanishing point, we can conclude that the "real version" of the line, in 3D before projection, goes right down the middle of the paper, parallel to the left and right sides. So, it intersects the top and bottom sides of the paper at their midpoints in the real world. Therefore, in the image the orange line also goes through the midpoints of the top and bottom sides of the paper. Note that none of the orange or blue lines actually intersect in "real life" since they are parallel to each other. They only intersect in the image because of their vanishing point.

<img src="intersections.png" width="640" alt="Intersections illustration">

We now have the center as well as the midpoints of the top and bottom sides of the paper. We can use the same method as above to find the midpoints of the left and right sides of the paper. Then we have 9 points which are kind of evenly spaced, in the sense that they essentially split up the A4 paper into 4 A6 papers. We can apply the above method to these smaller papers to find their midpoints and so on, to find even more evenly spaced points. This method can be repeated on the smaller "sub-papers" an arbitrary amount of times to find as many evenly spaced points as we want. Remember that for all these points, we have both their position in the image and in 3D on the real paper, so then we can simply color the paper in 3D with the colors of the pixels that the points are sitting on, and then this colored paper is what the program presents.


### Perspective correction, old version

We calibrate with the standard OpenCV function *calibrateCamera*, using the pixels of the paper corners and the center of the paper as the 2D image points. We define the paper to have its top left corner at the origin in 3D space, and simply place the other corners and the center of the paper at the appropriate distances from the origin. These corners and the center are used as the 3D object points in the calibration. The calibration gives us information about the camera itself (i.e. lens etc.) and its position and orientation in 3D space, which is all you need to calculate which pixel in the camera any 3D point is projected to/seen by. 

Using the definition for the real paper we made earlier, we can simply create a bunch of points in a grid on its surface in 3D space, project them into the camera and note which pixels they land on. If all the paper detection and calibration has been done perfectly up until this point, then the projected points will all land on pixels that are covered by the paper in the image. For each projected point, we color its corresponding point in the grid with the color of the pixel that it landed on. Then the paper grid will be colored according to the paper in the image. If we save this colored grid in a simple NumPy ndarray we can just display it using e.g. Pyplot.