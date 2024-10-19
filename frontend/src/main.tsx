import React from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import { Provider } from 'react-redux';
import '@gravity-ui/uikit/styles/styles.scss';
import './global.scss';
import { ThemeProvider, ToasterComponent, ToasterProvider } from '@gravity-ui/uikit';
import { store } from './store/store';

const container = document.getElementById('root');

if (container) {
  const root = createRoot(container);
  root.render(
    <ThemeProvider theme="light">
      <ToasterProvider >
        <Provider store={store}>
          <React.StrictMode>
            <App />
            <ToasterComponent />
          </React.StrictMode>
        </Provider>
      </ToasterProvider>
    </ThemeProvider>
  );
}