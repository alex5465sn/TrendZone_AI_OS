import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  retryCount: number;
}

function isExtensionDomNoise(error: Error): boolean {
  const msg = error?.message || '';
  return (
    (msg.includes('removeChild') || msg.includes('insertBefore') || msg.includes('appendChild')) &&
    msg.includes('not a child of this node')
  );
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, retryCount: 0 };

  static getDerivedStateFromError(error: Error): Partial<State> {
    if (isExtensionDomNoise(error)) {
      return { hasError: false };
    }
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    if (isExtensionDomNoise(error)) {
      if (this.state.retryCount < 3) {
        this.setState((prev) => ({ hasError: false, retryCount: prev.retryCount + 1 }));
      }
      return;
    }
    console.error('ErrorBoundary capturou um erro:', error, info);
  }

  handleReload = () => {
    this.setState({ hasError: false, retryCount: 0 });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 32, textAlign: 'center', fontFamily: 'sans-serif' }}>
          <h2>Ocorreu um erro inesperado na página.</h2>
          <p>Isso pode ter sido causado por uma extensão do navegador interferindo na página.</p>
          <p style={{ color: '#888', fontSize: 14 }}>
            Tente abrir em uma aba anônima (Ctrl+Shift+N) ou desativar extensões do navegador.
          </p>
          <button onClick={this.handleReload} style={{ padding: '8px 24px', marginTop: 16, cursor: 'pointer' }}>
            Recarregar
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
