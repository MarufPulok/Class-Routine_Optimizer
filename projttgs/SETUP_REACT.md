# React Integration Setup Guide

## Quick Start

1. **Install Node.js dependencies:**

```bash
cd projttgs/frontend
npm install
```

2. **Build React components:**

```bash
npm run build
```

3. **Start Django server:**

```bash
cd ..
python manage.py runserver
```

## Development Workflow

For development with auto-rebuild on file changes:

```bash
cd projttgs/frontend
npm run dev
```

Keep this running in a separate terminal while developing.

## How It Works

- **React & ReactDOM**: Loaded from CDN in `base.html` (for development)
- **Your Components**: Bundled by webpack into `static/js/react-components.js`
- **Integration**: Components auto-initialize via `data-react-component` attributes

## Adding New Components

1. Create component in `frontend/src/components/YourComponent.jsx`
2. Import in `frontend/src/index.js`:
   ```javascript
   import YourComponent from "./components/YourComponent";
   ```
3. Add to exports:
   ```javascript
   window.ReactComponents = {
     ExampleComponent,
     YourComponent, // Add here
     // ...
   };
   ```
4. Rebuild: `npm run build` (or use `npm run dev` for auto-rebuild)

## Using Components in Templates

### Method 1: Auto-initialization (Easiest)

```html
<div
  data-react-component="ExampleComponent"
  data-props='{"title": "My Title", "initialCount": 5}'
></div>
```

### Method 2: Manual initialization

```html
<div id="my-component"></div>
<script>
  const { ExampleComponent, createRoot, React } = window.ReactComponents;
  const root = createRoot(document.getElementById("my-component"));
  root.render(React.createElement(ExampleComponent, { title: "Hello" }));
</script>
```

## Example Template

See `templates/react_example.html` for a complete example.

## Notes

- React is loaded from CDN, so no need to bundle it
- Components are bundled separately for smaller file size
- Works with existing Django templates - no need to rewrite everything
- Can gradually add React components where needed
