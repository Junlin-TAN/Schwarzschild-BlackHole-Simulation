# Schwarzschild-BlackHole-Simulation 施瓦西黑洞模拟

This project provides a real-time, interactive simulation of a Schwarzschild black hole, demonstrating key gravitational phenomena such as gravitational lensing, the accretion disk, and the Doppler effect. The simulation is implemented in two versions: a desktop application using **Python/PyOpenGL** and a web-based version using **JavaScript/WebGL**.

The core rendering logic and shader framework are heavily inspired by and adapted from the excellent C++/OpenGL project [Blackhole by rossning92](https://github.com/rossning92/Blackhole). This project serves as a re-implementation and simplification, focusing on porting the complex shader logic to more accessible platforms like Python and WebGL.
![[Simulation Demo](black_hole_simulation_compressed.gif)
![[Simulation Demo](Cover.png)
![[Simulation Demo](Cover2.png)

## Key Features

- **Gravitational Lensing**: Simulates the bending of light paths around a massive object, causing the background starfield to appear distorted.
- **Accretion Disk**: A glowing, rotating disk of matter orbiting the black hole.
- **Doppler Effect (Relativistic Beaming)**: The side of the accretion disk moving towards the observer appears brighter and blue-shifted, while the side moving away appears dimmer and red-shifted.
- **Event Horizon**: The "point of no return," rendered as a perfect black sphere where no light can escape.
- **Photon Sphere**: At 1.5 times the Schwarzschild radius, light can orbit the black hole. This contributes to the complex visual effects near the event horizon.
- **Real-time and Interactive**: The simulation runs in real-time, allowing for future extensions like camera movement.

## How It Works: The Rendering Pipeline

This simulation doesn't use traditional 3D models. Instead, it employs a **screen-space ray marching** technique executed entirely on the GPU via a fragment shader. Here's a breakdown of the process for each pixel on the screen:

1.  **Backward Ray Tracing**: For every pixel, a light ray is cast *from* the camera *into* the scene. This is more efficient than tracing rays from light sources.

2.  **Numerical Integration**: The path of the light ray is not a straight line due to the black hole's gravity. We simulate its curved path using **Euler integration**. In a loop, we repeatedly update the ray's position and direction based on a simplified formula for gravitational attraction:

    ```glsl
    // This formula calculates the change in the ray's velocity (direction)
    // based on its proximity to the black hole.
    vec3 dr = -1.5 * Rs * ro / dot(ro, ro) / dot(ro, ro);

    // Update velocity and position over a small time step 'dt'
    rd += dr * dt; // rd is the ray direction
    ro += rd * dt; // ro is the ray origin/position
    ```

3.  **Collision Detection & Color Determination**: During the ray marching loop, we check for several conditions:
    - **Fell into Event Horizon**: If the ray's distance to the center is less than the Schwarzschild Radius (`Rs`), it has been captured. The pixel is colored **black**.
    - **Hit the Accretion Disk**: If the ray intersects the `y=0` plane within the disk's radius, we calculate the color based on a texture lookup. The previously mentioned Doppler effect is applied here to modify the color's brightness and hue.
    - **Escaped to Space**: If the ray travels far enough without hitting anything, it escapes the black hole's gravity. The pixel is colored by sampling a background skybox texture using the ray's final direction vector.

This entire process is repeated for every single pixel on the screen, for every frame, resulting in the final, fully rendered image.

---

## Implementations

This repository contains two separate implementations of the same shader logic.

### 1. Python / PyOpenGL Version

-   **Location**: Root directory (`/`)
-   **Description**: A desktop application that uses `PyOpenGL` for OpenGL bindings, `pygame` for window and event handling, and `numpy` for numerical operations.
-   **Dependencies**: `PyOpenGL`, `pygame`, `numpy`

### 2. JavaScript / WebGL Version

-   **Location**: `web/` directory
-   **Description**: A client-side web version that runs in any modern browser supporting WebGL. It uses minimal JavaScript to set up the canvas and run the GLSL shader.
-   **Dependencies**: A modern web browser.

## Acknowledgments

This project is a learning exercise and a tribute to the incredible work of **@rossning92**.

-   **Original Project**: [rossning92/Blackhole](https://github.com/rossning92/Blackhole)
-   The core GLSL shader logic, the ray marching algorithm, the physics formulas for gravitational lensing, and the overall rendering strategy are directly based on his excellent C++ implementation. My main contribution is the successful porting and adaptation of this logic into Python/PyOpenGL and JavaScript/WebGL environments.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
