import { Component, Suspense, useCallback, useState } from 'react';
import { createRoot } from 'react-dom/client';
import Lanyard from './Lanyard.jsx';
import PixelSwap from './PixelSwap.jsx';
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

function LanyardScene({ fallbackSrc }) {
  return (
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
}

function AboutReveal({ keyboardSrc, fallbackSrc }) {
  const [active, setActive] = useState(false);
  const [warming, setWarming] = useState(false);
  const [swapDone, setSwapDone] = useState(false);

  const onActiveChange = useCallback((next) => {
    if (!next) return;
    setActive(true);
    setWarming(true);
  }, []);

  const onComplete = useCallback((to) => {
    if (to) setSwapDone(true);
  }, []);

  return (
    <div className="about-reveal">
      <div className={'about-lanyard-host' + (swapDone ? ' is-live' : '')} id="about-lanyard">
        {warming ? <LanyardScene fallbackSrc={fallbackSrc} /> : null}
      </div>
      {swapDone ? null : (
        <PixelSwap
          className="about-pixel-swap"
          firstContent={
            <div className="about-keyboard-wrap">
              <img className="about-keyboard" src={keyboardSrc} alt="" />
              <div className="about-keyboard-fade" aria-hidden="true" />
            </div>
          }
          secondContent={<div className="about-pixel-blank" />}
          pixelSize={64}
          gap={0}
          pixelRadius={0}
          pixelSpin={0}
          pixelScale={0.35}
          duration={1400}
          pixelDuration={450}
          pattern="random"
          randomness={0}
          fade
          trigger="hover"
          active={active}
          onActiveChange={onActiveChange}
          onComplete={onComplete}
          style={{ width: '100%', height: '100%', aspectRatio: 'auto' }}
        />
      )}
    </div>
  );
}

window.mountAboutLanyard = function (el, opts) {
  if (!el) return;
  var fallbackSrc = (opts && opts.frontImage) || bundledPhoto;
  createRoot(el).render(<LanyardScene fallbackSrc={fallbackSrc} />);
};

window.mountAboutPixelSwap = function (el, opts) {
  if (!el) return;
  var keyboardSrc = (opts && opts.keyboardSrc) || 'source/pics/keyboard.jpg';
  var fallbackSrc = (opts && opts.frontImage) || bundledPhoto;
  createRoot(el).render(<AboutReveal keyboardSrc={keyboardSrc} fallbackSrc={fallbackSrc} />);
};
