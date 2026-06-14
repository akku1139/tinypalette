# tinypalette

tinygrad WebUI

## Usage

```sh
pnpm setup
pnpm build
DEV=CL RUSTICL_FEATURES=fp64 pnpm start
```

## Config

`~/.config/tinypalette/config.json`

```json
{
  "path": {
    "models": {
      "sd": "/path/to/StableDiffusion/models"
    },
    "outputs": {
      "image": "/path/to/image/dir"
    }
  }
}
```
