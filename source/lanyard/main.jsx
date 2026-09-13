import { Component, Suspense } from 'react';
import { createRoot } from 'react-dom/client';
import Lanyard from './Lanyard.jsx';
import bundledPhoto from '../bage_photo.jpg';
import './Lanyard.css';

class LanyardErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { failed: false };
  }
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    if (this.state.failed) return this.props.fallback;
    return this.props.children;
  }
}

window.mountAboutLanyard = function (el, opts) {
  if (!el) return;
  var fallbackSrc = (opts && opts.frontImage) || bundledPhoto;
  createRoot(el).render(
    <LanyardErrorBoundary
      fallback={<img className="about-lanyard-fallback" src={fallbackSrc} alt="Yuting Feng" />}
    >
      <Suspense fallback={null}>
        <Lanyard
          position={[0, 0, 10]}
          gravity={[0, -40, 0]}
          fov={20}
          transparent={true}
          frontImage={bundledPhoto}
          imageFit="cover"
        />
      </Suspense>
    </LanyardErrorBoundary>
  );
};
