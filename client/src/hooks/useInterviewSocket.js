import { useEffect, useRef } from 'react';

function getWsBase() {
  const envUrl = import.meta.env.VITE_WS_BASE_URL;
  const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  if (!envUrl) {
    return `${proto}//${window.location.host}/ws`;
  }
  if (envUrl.startsWith('ws://') || envUrl.startsWith('wss://')) {
    return envUrl.replace(/\/$/, '');
  }
  const cleanPath = envUrl.startsWith('/') ? envUrl : `/${envUrl}`;
  return `${proto}//${window.location.host}${cleanPath}`;
}

export function useInterviewSocket(id, token, onEvent) {
  const ref = useRef(null);
  useEffect(() => {
    if (!id || !token) return;
    let stopped = false, timer;
    const connect = () => {
      if (stopped || !navigator.onLine) return;
      const base = getWsBase();
      const ws = new WebSocket(`${base}/interviews/${id}?token=${encodeURIComponent(token)}`);
      ref.current = ws;
      ws.onmessage = (e) => onEvent(JSON.parse(e.data));
      ws.onclose = () => {
        if (!stopped) timer = setTimeout(connect, 2000);
      };
    };
    connect();
    return () => {
      stopped = true;
      clearTimeout(timer);
      ref.current?.close();
    };
  }, [id, token]);

  return (e) => ref.current?.readyState === 1 && ref.current.send(JSON.stringify(e));
}
