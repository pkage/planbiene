
import React, { Component } from "react";
import ReactDOM from "react-dom";
import * as THREE from 'three';
import ThreeGlobe from "three-globe";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";

class Globe extends Component {

    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.sceneSetup();
        this.addCustomSceneObjects();
        this.startAnimationLoop();
        this.generateCoordinates();
        window.addEventListener('resize', this.handleWindowResize);
    }
    
    sceneSetup = () => {
      // get container dimensions and use them for scene sizing
      const width = this.el.clientWidth;
      const height = this.el.clientHeight;

      
      this.scene = new THREE.Scene();

      // Setup camera
      this.camera = new THREE.PerspectiveCamera();
      this.camera.aspect = window.innerWidth/window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.camera.position.z = 301;


      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
      this.el.appendChild( this.renderer.domElement ); // mount using React ref



      this.controls = new OrbitControls( this.camera, this.el );
      this.controls.minDistance = 150;
      this.controls.rotateSpeed = 5;
      this.controls.zoomSpeed = 0.8;

    };
    addCustomSceneObjects  = () => {

      const coords = [{"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 38.880099, "endLng": -77.026165, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 43.111606, "endLng": -75.592926, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 41.4783608, "endLng": -71.9630872, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 32.77478601, "endLng": -117.0712325, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 40.752664, "endLng": -73.994309, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 40.752664, "endLng": -73.994309, "color": "green"}, {"startLat": 41.394378662109375, "startLng": 2.1131200790405273, "endLat": 40.752664, "endLng": -73.994309, "color": "green"}]
      const arcsData = coords
      var pointsData = coords.map((e) => {
            return {
              lat: e.endLat,
              lng: e.endLng,
              size: 0.1,
              color: "green"
            }
      });

        pointsData.push({
            lat: coords[0].startLat,
            lng: coords[0].startLng,
            size: 0.15,
            color: "blue"
      });
        
      const Globe = new ThreeGlobe()
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
            .arcsData(arcsData).pointsData(pointsData).pointColor("color").pointAltitude('size')
            .arcColor('color').arcStroke(2).arcsTransitionDuration(3000);
      
      this.scene.add(Globe);
      this.scene.background = new THREE.Color( '#232528' );
      this.scene.add(new THREE.AmbientLight(0xbbbbbb));
      this.scene.add(new THREE.DirectionalLight(0xffffff, 0.6));

    };
    startAnimationLoop = () => {

      this.controls.update();
      this.renderer.render(this.scene, this.camera);
      this.requestID = window.requestAnimationFrame(this.startAnimationLoop);
    };

    handleWindowResize = () => {
      const width = this.el.clientWidth;
      const height = this.el.clientHeight;
  
      this.renderer.setSize( width, height );
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
    };

    generateCoordinates = () => {
      let usr = this.props.user_data;
      let res = this.props.results;
      return Object.values(res).map((e) => {
        return {
          startLat : usr.latitude,
          startLng : usr.longitude,
          endLat : e[0]["venue"]["longitude"],
          endLng : e[0]["venue"]["latitude"],
          color : "green"
        }
      })
    }
    
    render() {
        return <div ref={ref => (this.el = ref)} />;
    }
}

export default Globe;
