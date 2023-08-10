const { spawn } = require('child_process');
const debug = require('debug');
const log = debug('weasyprint:log');
const err = debug('weasyprint:error');

const dasher = input => input
    .replace(/\W+/g, '-')
    .replace(/([a-z\d])([A-Z])/g, '$1-$2')
    .toLowerCase();

const quote = val => (typeof val === 'string' && process.platform !== 'win32')
    ? '"' + val.replace(/(["\\$`])/g, '\\$1') + '"'
    : val;

const weasyprint = async (input, { command = 'weasyprint', ...opts } = {}) => {
    let child;
    const isUrl = /^(https?|file):\/\//.test(input);
    const keys = Object.keys(opts);
    const args = [command];

    keys.forEach((key, index, arry) => {
        arry[index] = key.length === 1 ? '-' + key : '--' + dasher(key);
    });

    args.push(isUrl ? quote(input) : '-'); // stdin if HTML given directly
    args.push(opts.output ? quote(opts.output) : '-'); // stdout if no output file

    log('Spawning %s with args %o...', args[0], args);
    if (process.platform === 'win32') {
        child = spawn(args[0], args.slice(1));
    } else {
        child = spawn('/bin/sh', ['-c', args.join(' ') + ' | cat']);
    }

    // write input to stdin if it isn't a url
    if (!isUrl) child.stdin.end(input);

    return new Promise((resolve, reject) => {
        const buffers = [];
        const errBuffers = [];
        child.stdout.on('data', chunk => {
            buffers.push(Buffer.from(chunk));
        });
        child.stderr.on('data', chunk => {
            errBuffers.push(Buffer.from(chunk));
            err(chunk.toString('utf8').trim());
        });
        child.on('exit', function () {
            if (buffers.length !== 0) {
                log('Success, returning PDF buffer...');
                resolve(Buffer.concat(buffers));
            } else {
                reject(new Error(Buffer.concat(errBuffers).toString('utf8')));
            }
        });
    });
}

module.exports = weasyprint;
