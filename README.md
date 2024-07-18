# `root-ca-downloader`

## Overview

`root-ca-downloader` is a Python tool designed to fetch and convert SSL/TLS
certificate chains from a specified URL into both PEM and C header file formats.
This tool simplifies the process of integrating SSL/TLS certificates into
applications that require hardcoded certificates.

## Setup

```sh
git clone https://github.com/xyzshantaram/root-ca-downloader.git
cd root-ca-downloader
pip install -r requirements.txt
```

## Usage

```sh
python3 get_root_ca.py https://example.com
```

The chain is saved to `example_com.pem` and `example_com.h`. `example_com.h`
contains a C string called EXAMPLE_COM_CERT.

You can use it in your Arduino sketch with:

```cpp
#include "example_com.h"

// ...

NetworkClientSecure *client = new NetworkClientSecure;
if (client) {
  client->setCACert(EXAMPLE_COM_CERT);
}
```

## License

Copyright (c) 2024 Siddharth S Singh (me@shantaram.xyz), under the terms of
[the MIT License](./LICENSE.md).
