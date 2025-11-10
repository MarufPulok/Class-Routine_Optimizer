# Frontend React Components

This directory contains React components that can be embedded in Django templates.

## Setup

1. Install Node.js and npm if you haven't already.

2. Install dependencies:
```bash
cd frontend
npm install
```

3. Build React components:
```bash
npm run build
```

For development with auto-rebuild:
```bash
npm run dev
```

## Usage in Django Templates

### Method 1: Using data attributes (Auto-initialization)

Add a React component to any Django template:

```html
{% load static %}

<div 
  data-react-component="ExampleComponent"
  data-props='{"title": "My Component", "initialCount": 5}'
></div>
```

### Method 2: Manual initialization

```html
{% load static %}

<div id="my-react-component"></div>

<script>
  const { ExampleComponent, createRoot, React } = window.ReactComponents;
  const root = createRoot(document.getElementById('my-react-component'));
  root.render(React.createElement(ExampleComponent, {
    title: 'My Component',
    initialCount: 5
  }));
</script>
```

## Adding New Components

1. Create a new component in `src/components/YourComponent.jsx`
2. Import it in `src/index.js`
3. Add it to `window.ReactComponents` export
4. Rebuild: `npm run build`

## Development vs Production

- **Development**: Uses React from CDN (already included in base.html)
- **Production**: Uses built bundle from `static/js/react-components.js`

Make sure to run `npm run build` before deploying to production.

