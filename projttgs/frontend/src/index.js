// React components entry point
// Import and export all React components here
// React and ReactDOM are external (loaded from CDN in base.html)

import React from 'react';
import { createRoot } from 'react-dom/client';

// Example component - you can add more components here
import ExampleComponent from './components/ExampleComponent';

window.ReactComponents = {
  ExampleComponent,
  createRoot,
  React,
};

// Auto-initialize components with data-react-component attribute
document.addEventListener('DOMContentLoaded', () => {
  const components = document.querySelectorAll('[data-react-component]');
  components.forEach((element) => {
    const componentName = element.getAttribute('data-react-component');
    const props = JSON.parse(element.getAttribute('data-props') || '{}');
    
    if (window.ReactComponents[componentName]) {
      const Component = window.ReactComponents[componentName];
      const root = window.ReactComponents.createRoot(element);
      root.render(React.createElement(Component, props));
    }
  });
});

