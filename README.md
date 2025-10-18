
# Interactive Black Hole Simulation: Schwarzschild & Kerr Black Hole

![Kerr Black Hole Demo](gif/blackhole_recording0.gif)

This project provides a real-time, interactive simulation of both a static **Schwarzschild black hole** and a rotating **Kerr black hole**. It demonstrates key phenomena predicted by General Relativity, such as gravitational lensing, the accretion disk, the relativistic Doppler effect, and the incredible **frame-dragging** effect of a spinning black hole.

The core rendering logic and shader framework were initially inspired by the excellent C++/OpenGL project [Blackhole by rossning92](https://github.com/rossning92/Blackhole). However, this project has since evolved into a complete, physically-robust implementation featuring a switchable physics core that allows for the direct comparison between static and rotating black holes.

A key goal of this project is to make this complex simulation more accessible and significantly easier to run. The Python version is platform-independent and requires no compilation, effectively lowering the barrier for anyone wishing to experience or experiment with these fascinating cosmic objects.

### Kerr Black Hole (Rotating) - The Final Result!
![Kerr Black Hole Demo](gif/blackhole_recording1.gif)
![Kerr Black Hole Demo](gif/blackhole_recording2.gif)
![Kerr Black Hole Demo](gif/blackhole_recording3.gif)
![Kerr Black Hole Demo](gif/blackhole_recording4.gif)
![Kerr Black Hole Demo](gif/blackhole_recording5.gif)
![Kerr Black Hole Demo](gif/blackhole_recording6.gif)
![Kerr Black Hole Demo](gif/blackhole_recording7.gif)
![Kerr Black Hole Demo](gif/blackhole_recording8.gif)

## Key Features

-   **Dual Physics Cores**: Seamlessly switch between a **Schwarzschild (static)** and a **Kerr (rotating)** black hole simulation with the press of a button.
-   **Frame-Dragging (Lense-Thirring Effect)**: Witness the mind-bending "spacetime vortex" around the Kerr black hole, which drags and twists the accretion disk and background starlight from any viewing angle.
-   **Extreme Relativistic Beaming**: The side of the accretion disk moving towards the observer becomes intensely bright, while the side moving away fades into darkness, accurately modeled using the orbital velocities of a Kerr spacetime.
-   **Gravitational Lensing**: Simulates the bending of light paths, causing the background starfield to appear distorted and creating multiple images of the accretion disk (e.g., the "light arch" over the top).
-   **Deformed Event Horizon Shadow**: Observe how the black hole's shadow deforms from a perfect circle (Schwarzschild) to a "D" shape (Kerr) due to frame-dragging.
-   **Physically-Accurate Accretion Disk**: The disk's inner radius and orbital velocities are correctly modeled based on the black hole's spin, respecting the **Innermost Stable Circular Orbit (ISCO)**.
-   **Real-time and Interactive**: The simulation is fully interactive, allowing you to move the camera, and toggle visual components on the fly.

## Interaction Guide 

-   **Mouse**: Click and drag to rotate the camera around the black hole.
-   **Mouse Wheel**: Zoom in and out.
-   **`SPACE` Key**: Toggle the accretion disk on/off.
-   **`S` Key**: Switch between the Schwarzschild (static) and Kerr (rotating) physics models.
-   **`P` Key**: Toggle the manually-drawn photon sphere effect (only for the Schwarzschild model).

## How It Works: The Rendering Pipeline

This simulation uses a **screen-space ray marching** technique executed entirely on the GPU via a fragment shader.

1.  **Backward Ray Tracing**: For each pixel, a light ray is cast *from* the camera *into* the scene.

2.  **Numerical Integration (4th Order Runge-Kutta)**: The path of the light ray is curved by gravity. We simulate this path with high precision using the **4th Order Runge-Kutta (RK4) method**. In a loop, we repeatedly update the ray's position and velocity based on a unified acceleration formula.

3.  **Collision Detection & Color Determination**: During the ray marching loop:
    -   **Fell into Event Horizon**: If the ray's distance is less than the horizon radius (which differs for Schwarzschild and Kerr), the pixel is colored **black**.
    -   **Hit the Accretion Disk**: If the ray intersects the `y=0` plane, we calculate the color based on a noise texture and the physically-correct Doppler and gravitational redshift effects.
    -   **Escaped to Space**: If the ray travels far enough, the pixel is colored by sampling a background skybox texture.

## Core Principles & Mathematical Formulas 

This simulation is based on the physical phenomena described by **General Relativity**, which are approximated using **numerical methods** within the fragment shader.

### 1. Gravitational Model
We use a single, unified function to calculate the acceleration of a light ray, which adapts based on whether the black hole is rotating.

#### a) Schwarzschild Gravity (Post-Newtonian Approximation)

For a static black hole, the acceleration includes the standard Newtonian gravity plus a first-order relativistic correction term, which is crucial for correctly simulating light bending.

$$
\vec{a}_{\text{Schwarzschild}} = - \frac{M}{|\vec{p}|^3}\vec{p} \left( 1 + \frac{3|\vec{L}|^2}{|\vec{p}|^2} \right)
$$

Where:
-   $M$ is the mass of the black hole.
-   $\vec{p}$ is the photon's position vector.
-   $\vec{L} = \vec{p} \times \vec{v}$ is the photon's specific angular momentum.

```glsl
vec3 acc_schwarzschild = -M * pos / pow(r, 3.0) * (1.0 + 3.0 * dot(cross(pos, vel), cross(pos, vel)) / (r2));
```

#### b) Frame-Dragging (Gravitomagnetism)

For a rotating Kerr black hole, we add an additional acceleration term that models the Lense-Thirring (frame-dragging) effect. This term acts like a "gravitational Lorentz force," creating the spacetime vortex.

$$
\vec{a}_{\text{drag}} \approx - \frac{6M}{|\vec{p}|^3} (\vec{v} \times \vec{J})
$$

Where:
-   $\vec{J}$ is the angular momentum vector of the black hole (pointing along its spin axis).
-   $\vec{v}$ is the velocity of the photon.
-   The cross product `(v x J)` ensures the force is perpendicular to both the photon's motion and the spin axis, creating the characteristic swirl.

```glsl

if (u_kerr_enabled) {
    vec3 J = vec3(0, a * M, 0); 
    float r3 = r2 * r;
    vec3 acc_drag = -(6.0 * M / r3) * cross(vel, J);
    
    return acc_schwarzschild + acc_drag;
}
```

### 2. Numerical Integration: 4th Order Runge-Kutta (RK4)

To ensure stability and accuracy, especially in the extreme gravity near the event horizon, we use the **RK4 method** to integrate the ray's path. Unlike the simpler Euler method, RK4 takes four samples of the acceleration within each time step to calculate a weighted average, dramatically reducing error and preventing visual artifacts.

$$
\begin{aligned}
\vec{k}_{v1} &= \Delta t \cdot \vec{a}(\vec{p}_i, \vec{v}_i) \\
\vec{k}_{p1} &= \Delta t \cdot \vec{v}_i \\
\vec{k}_{v2} &= \Delta t \cdot \vec{a}(\vec{p}_i + \frac{\vec{k}_{p1}}{2}, \vec{v}_i + \frac{\vec{k}_{v1}}{2}) \\
\vec{k}_{p2} &= \Delta t \cdot (\vec{v}_i + \frac{\vec{k}_{v1}}{2}) \\
\vec{k}_{v3} &= \Delta t \cdot \vec{a}(\vec{p}_i + \frac{\vec{k}_{p2}}{2}, \vec{v}_i + \frac{\vec{k}_{v2}}{2}) \\
\vec{k}_{p3} &= \Delta t \cdot (\vec{v}_i + \frac{\vec{k}_{v2}}{2}) \\
\vec{k}_{v4} &= \Delta t \cdot \vec{a}(\vec{p}_i + \vec{k}_{p3}, \vec{v}_i + \vec{k}_{v3}) \\
\vec{k}_{p4} &= \Delta t \cdot (\vec{v}_i + \vec{k}_{v3}) \\
\vec{p}_{i+1} &= \vec{p}_i + \frac{1}{6}(\vec{k}_{p1} + 2\vec{k}_{p2} + 2\vec{k}_{p3} + \vec{k}_{p4}) \\
\vec{v}_{i+1} &= \vec{v}_i + \frac{1}{6}(\vec{k}_{v1} + 2\vec{k}_{v2} + 2\vec{k}_{v3} + \vec{k}_{v4})
\end{aligned}
$$

```glsl
vec3 k1_vel = DT * get_acceleration(ray_pos, velocity);
vec3 k1_pos = DT * velocity;

vec3 k2_vel = DT * get_acceleration(ray_pos + k1_pos * 0.5, velocity + k1_vel * 0.5);
vec3 k2_pos = DT * (velocity + k1_vel * 0.5);

vec3 k3_vel = DT * get_acceleration(ray_pos + k2_pos * 0.5, velocity + k2_vel * 0.5);
vec3 k3_pos = DT * (velocity + k2_vel * 0.5);

vec3 k4_vel = DT * get_acceleration(ray_pos + k3_pos, velocity + k3_vel);
vec3 k4_pos = DT * (velocity + k3_vel);

ray_pos += (k1_pos + 2.0 * k2_pos + 2.0 * k3_pos + k4_pos) / 6.0;
velocity += (k1_vel + 2.0 * k2_vel + 2.0 * k3_vel + k4_vel) / 6.0;
```

### 3. Kerr Accretion Disk Physics 

The extreme brightness of the Kerr disk's approaching side is due to the physically accurate orbital velocity of the gas. For a particle in a prograde (co-rotating) orbit in the equatorial plane of a Kerr black hole, the angular velocity is:

$$
\Omega = \frac{\sqrt{M}}{r^{3/2} + a\sqrt{M}}
$$

Where:
-   $r$ is the orbital radius.
-   $a$ is the black hole's spin parameter.

This formula shows that as spin `a` increases, the orbital velocity `v = Ωr` becomes much higher than in the Schwarzschild case (`a=0`), leading to a far more dramatic Doppler effect.

```glsl
float omega = sqrt(M) / (pow(r_cyl, 1.5) + a * sqrt(M));
float v_mag = omega * r_cyl;
```
--
## Acknowledgments 

This project's journey began with the inspiration from the incredible work of **@rossning92**. The initial idea to use screen-space ray marching and the foundational shader structure were adapted from his excellent C++ project:

-   **Inspirational Project**: [rossning92/Blackhole](https://github.com/rossning92/Blackhole)

However, through a long and intensive process of debugging, research, and iteration, this project has evolved significantly from its original starting point. The core physics models for both Schwarzschild and Kerr black holes, the 4th-order Runge-Kutta numerical integrator, and the stable, gimbal-lock-free camera system are **entirely new implementations** developed during the course of this project to achieve a higher degree of physical accuracy and numerical stability.

We remain grateful to the original project for providing the foundational spark for this deep dive into computational astrophysics.

--
## References and Further Reading 

### Project Inspiration 

-   **rossning92/Blackhole**
    -   `https://github.com/rossning92/Blackhole`

### Key Physical and Computational Concepts 

-   **Image of a Spherical Black Hole with a Thin Accretion Disk (J.P. Luminet, 1979)**
    -   `https://ui.adsabs.harvard.edu/abs/1979A&A....75..228L/abstract`

-   **The Lense-Thirring / Frame-Dragging Effect (NASA Overview)**
    -   `https://science.nasa.gov/science-news/science-at-nasa/2004/26apr_frame`

-   **Post-Newtonian Formalism (Wikipedia)**
    -   `https://en.wikipedia.org/wiki/Post-Newtonian_formalism`

-   **Runge–Kutta Methods (Wikipedia)**
    -   `https://en.wikipedia.org/wiki/Runge–Kutta_methods`

### Developmental Reference 

-   **Geodesics in the Kerr Spacetime (T. Gantumur, McGill University)**
    -   `https://math.mcgill.ca/gantumur/math599w17/project-kerr.pdf`

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
```




