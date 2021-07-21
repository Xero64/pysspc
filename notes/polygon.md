# General Polygon Calculations

## Area

$$
A = \frac{1}{2}\sum_{i=1}^{n} \left( y_i z_{i+1} - y_{i+1} z_i \right)
$$

https://en.wikipedia.org/wiki/Polygon#Area

## First Moment of Area

$$
A_y = \frac{1}{6}\sum_{i=1}^{n} \left( y_i + y_{i+1} \right) \left( y_i z_{i+1} - y_{i+1} z_i \right)
$$

$$
A_z = \frac{1}{6}\sum_{i=1}^{n} \left( z_i + z_{i+1} \right) \left( y_i z_{i+1} - y_{i+1} z_i \right)
$$

https://en.wikipedia.org/wiki/Polygon#Centroid

## Centroid

$$
c_y = \frac{A_y}{A}
$$
$$
c_z = \frac{A_z}{A}
$$

https://en.wikipedia.org/wiki/Polygon#Centroid

## Second Moment of Area

$$
A_{yy} = \frac{1}{12}\sum_{i=1}^{n} \left( y_i^2 + y_i y_{i+1} + y_{i+1}^2 \right) \left( y_i z_{i+1} - y_{i+1} z_i\right)
$$

$$
A_{zz} = \frac{1}{12}\sum_{i=1}^{n} \left( z_i^2 + z_i z_{i+1} + z_{i+1}^2 \right) \left( y_i z_{i+1} - y_{i+1} z_i\right)
$$

$$
A_{yz} = \frac{1}{24}\sum_{i=1}^{n} \left( y_i z_{i+1} + 2 y_i z_i + 2 y_{i+1} z_{i+1} + y_{i+1} z_i \right) \left( y_i z_{i+1} - y_{i+1} z_i \right)
$$

https://en.wikipedia.org/wiki/Second_moment_of_area#Any_polygon

### Parallel Axis Theorem

$$
I_{yy} = A_{zz}-A c_z^2
$$

$$
I_{zz} = A_{yy}-A c_y^2
$$

$$
I_{yz} = A_{yz}-A c_y c_z
$$

### Second Moment of Area Principle Angle and Transformation

$$
\theta_p = \frac{1}{2}\arctan{\left( \frac{2 I_{yz}}{I_{zz}-I_{yy}} \right)}
$$

$$
I'_{yy} = I_{yy}\cos^2{\theta}+I_{zz}\sin^2{\theta}+2I_{yz}\sin{\theta}\cos{\theta}
$$

$$
I'_{zz} = I_{yy}\sin^2{\theta}+I_{zz}\cos^2{\theta}-2I_{yz}\sin{\theta}\cos{\theta}
$$

$$
I'_{yz} = I_{yz} \left( \cos^2{\theta}-\sin^2{\theta} \right) - \left( I_{zz}-I_{yy} \right) \sin{\theta} \cos{\theta}
$$
