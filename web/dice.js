import * as THREE from "https://cdnjs.cloudflare.com/ajax/libs/three.js/0.155.0/three.module.min.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.155.0/examples/jsm/loaders/GLTFLoader.js";

// Desired dice result (1 to 6)
const DESIRED_RESULT = 6;

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Light
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);

// Floor
const floorGeometry = new THREE.PlaneGeometry(10, 10);
const floorMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa });
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
scene.add(floor);

// Load Dice Model
const loader = new GLTFLoader();
loader.load(
  "dice.gltf", // Replace with the path to your 3D dice model
  (gltf) => {
    const dice = gltf.scene;
    dice.scale.set(1, 1, 1);
    dice.position.set(0, 1, 0);
    scene.add(dice);

    // Animate Dice Roll
    let rolling = true;
    let timer = 0;
    const rollDuration = 2; // Duration of the roll in seconds
    const fps = 60; // Animation frames per second

    function animate() {
      requestAnimationFrame(animate);

      if (rolling) {
        // Simulate dice rolling with random rotation
        dice.rotation.x += Math.random() * 0.2;
        dice.rotation.y += Math.random() * 0.2;
        dice.rotation.z += Math.random() * 0.2;

        timer += 1 / fps;

        // Stop rolling after the duration
        if (timer >= rollDuration) {
          rolling = false;

          // Set final orientation for the desired result
          const faceRotations = {
            1: { x: Math.PI / 2, y: 0, z: 0 },
            2: { x: 0, y: 0, z: Math.PI / 2 },
            3: { x: 0, y: 0, z: Math.PI },
            4: { x: 0, y: Math.PI, z: Math.PI },
            5: { x: 0, y: 0, z: -Math.PI / 2 },
            6: { x: -Math.PI / 2, y: 0, z: 0 },
          };
          const finalRotation = faceRotations[DESIRED_RESULT];
          dice.rotation.set(finalRotation.x, finalRotation.y, finalRotation.z);
        }
      }

      renderer.render(scene, camera);
    }

    animate();
  },
  undefined,
  (error) => {
    console.error("An error occurred while loading the dice model:", error);
  }
);

// Camera Position
camera.position.z = 5;
