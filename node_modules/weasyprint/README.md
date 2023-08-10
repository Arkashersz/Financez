# weasyprint

*A NodeJS wrapper module for Weasyprint Python package (HTML to PDF converter).*

This module is a fork of [dills122/weasyprint-wrapper](https://github.com/dills122/weasyprint-wrapper) with fixes, minor updates and reuploaded back to npm as [weasyprint](https://www.npmjs.com/package/weasyprint).

## Getting started
Install the package (Python3 required):
```
pip3 install weasyprint
```

Add this NodeJS wrapper to your project:
```
npm i weasyprint
```

## Usage
Example:

```javascript
const weasyprint = require('weasyprint');

// URL, specifying the format & default command to spawn weasyprint
const resBuffer = await weasyprint('http://google.com/', { 
    command: '~/programs/weasyprint',
    pageSize: 'letter'
});
  
// HTML
const resbuffer = await weasyprint('<h1>Test</h1><p>Hello world</p>');

// Save in a file
try {
    const buffer = await weasyprint('<h1>Test</h1><p>Hello world</p>');
    fs.writeFileSync('test.pdf', buffer);
} catch (err) {
    console.error(err);
}
```

## License
MIT
