# Yakut

[![Build status](https://ci.appveyor.com/api/projects/status/knl63ojynybi3co6/branch/main?svg=true)](https://ci.appveyor.com/project/Zubax/yakut/branch/main)
[![PyPI - Version](https://img.shields.io/pypi/v/yakut.svg)](https://pypi.org/project/yakut/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Forum](https://img.shields.io/discourse/users.svg?server=https%3A%2F%2Fforum.uavcan.org&color=1700b3)](https://forum.uavcan.org)

Yakút 간단한 커맨드 라인 인터페이스 도구로 UAVCAN 네트워크 진단 및 디버깅에 사용한다.
[PyUAVCAN](https://github.com/UAVCAN/pyuavcan) 기반으로 모든 UAVCAN transports(UDP, serial, CAN, ...)을 지원하며 프로토콜의 모든 주요 특징과 호환된다.
Linux, Windows, macOS에서 사용이 가능하다.

<img src="/docs/monitor.png" alt="yakut monitor">

Ask questions and get assistance at [forum.uavcan.org](https://forum.uavcan.org/).

## Installing

먼저 **Python 3.7 이후 버전** 이 설치되어 있어야 한다. 

Yakut 설치 : **`pip install yakut`**

문서 읽기 : **`yakut --help`**

새로운 버전 체크 : **`pip install --upgrade yakut`**

Windows, Linux에서 설치 및 설정 : [포럼](https://forum.uavcan.org/t/screencast-of-installing-configuring-yakut/1197)

### GNU/Linux

조이스틱 사용을 원하는 경우 SDL2 수동 설치.
일반적으로 패키지 이름은 `libsdl2`이다.
MIDI 제어기는 ALSA API library가 필요할 수도 있다.

## Invoking commands

옵션으로 명령 라인 인자 혹은 환경 변수를 줄 수 있으며 이 경우 형식은 `YAKUT_[subcommand_]option` 와 같다.
만약 2개 모두 필요한 경우 커맨드 라인 옵션이 먼저 오고 이후에 환경 변수가 온다.
기본 설정으로 사용하려면 사용하는 쉘에서 환경 변수를 export해서 설정할 수 있다.

Yakut를 호출할때 메인 명령에 대한 옵션은 서브 커맨드 전에 지정해야 한다. :

```bash
yakut --path=/the/path compile path/to/my_namespace --output=destination/directory
```

이 예제에서 관련 환경 변수는 `YAKUT_PATH` 와 `YAKUT_COMPILE_OUTPUT` 이다.

`yakut compile`과 같은 서브 커맨드는 짧게 `yakut com`로 사용할 수 있다.

모든 서브 커맨드에 대해서 `--help` 옵션이 있다.

Yakut는 다른 설치 프로그램과 충돌이 되지 않는다면 **`y`**와 같은 alias로 호출할 수도 있다.

## Compiling DSDL

사용할려는 custom DSDL 네임스페이스을 가지고 있다고 가정해보자.
먼저 *compiled*이 필요하다:

```bash
yakut compile ~/custom_data_types/sirius_cyber_corp
```

명령의 대부분은 유효한 표준 네임스페이스가 필요하고 역시 컴파일이 필요하다. :

```bash
yakut compile  ~/public_regulated_data_types/uavcan  ~/public_regulated_data_types/reg
```

컴파일 출력은 현재 작업 디렉토리에 저장되지만 필요하다면 `--output` 나 `YAKUT_COMPILE_OUTPUT`로 변경할 수 있다.
Yakut은 출력 결과물이 어디에 위치하는지 알고 있어야 한다;
기본적으로는 현재 디렉토리에서 찾는다.
추가로 `--path` 나 `YAKUT_PATH`를 사용해서 위치를 검색할 수 있다.

여기서 올 수 있는 첫번째 질문:
*미리 컴파일된 regulated DSDL를 tool과 함께 배포하지 않는가?*
사실 그렇게 하는 것은 그리 어렵지 않다. 하지만 벤더 지정과 정규 DSDL을 동일한 레벨에서 지원하기 위한 약속을 강조할려는 목적으로 피하고 있다.
과거에 정규 네임스페이스를 특별히 취급했었는데 이로 인해 DSDL의 목적을 잘못 이해하게 되었었다.
특히 벤더 지정 타입으로 확장된 표준 네임스페이스의 fork는 에코시스템에 좋지 않은 영향을 미친다.

정규 네임스페이스를 수동으로 컴파일하는 것은 이슈가 되지 않는다. 왜냐하면 실행할 하나의 명령이기 때문이다.
컴파일된 네임스페이스를 유지하기로 선택해서 특정 디렉토리에 넣어 두고 `YAKUT_PATH=/your/directory`를 쉘 rc파일에 추가하면 Yakut를 호출할때 해당 path를 수동으로 지정하지 않아도 된다.
유사하게 컴파일된 DSDL을 위한 기본 목적지로 해당 디렉토리를 사용하기 위해서 이를 설정할 수 있다.:

```bash
# bash/zsh on GNU/Linux or macOS
export YAKUT_COMPILE_OUTPUT=~/.yakut
export YAKUT_PATH="$YAKUT_COMPILE_OUTPUT"
```

```powershell
# PowerShell on Windows (double quotes are always required!)
$env:YAKUT_COMPILE_OUTPUT="$env:APPDATA\Yakut"
$env:YAKUT_PATH="$env:YAKUT_COMPILE_OUTPUT"
```

단순하게 `yakut compile path/to/my_namespace`하면 출력물이 항상 특정 장소로부터 읽고 쓰기가 가능하게 된다.

## Communicating

네트워크에 접속하는 명령은 어떻게 그렇게 동작하는지 알아야 한다.
이를 설정하는 2가지 방식:
*UAVCAN registers*를 환경 변수를 통해서 전달(이것이 기본)하거나
 혹은 초기에 `--transport`/`YAKUT_TRANSPORT`를 통해서 전달한다.(이 경우 해당 레지스터들은 무시된다)
후자는 일반적으로 추천하지 않으므로 첫번째 것에 초점을 둔다.

UAVCAN 레지스터는 UAVCAN 어플리케이션/노드의 여러 설정 파라미터를 포함하고 있는 이름있는 값이다.
이것들은 [UAVCAN Specification](https://uavcan.org/specification)에서 추가로 설정한다.
새로운 프로세스가 구동되면, 환경 변수를 통해서 임의의 레지스터를 전달하는 것이 가능하다.

네트워크에 연결하는 방법을 결정하기 위해서 UAVCAN 노드가 지켜보는 레지스터들이 있다.
이들 중에 일부는 아래와 같다.
지원하는 레지스터의 모든 설명은 [`pyuavcan.application.make_transport()`](https://pyuavcan.readthedocs.io/en/stable/api/pyuavcan.application.html#pyuavcan.application.make_transport)을 위한 API 문서에서 확인할 수 있다.

만약 유효한 레지스터들이 1개 트랜스포트 이상의 설정을 가진다면 추가 트랜스포트는 초기화 된다.

Transport |Register name        |Register type  |Environment variable name|Semantics                                          |Example environment variable value
----------|---------------------|---------------|-------------------------|---------------------------------------------------|------------------------------------
All       |`uavcan.node.id`     |`natural16[1]` |`UAVCAN__NODE__ID`       |The local node-ID; anonymous if not set            |`42`
UDP       |`uavcan.udp.iface`   |`string`       |`UAVCAN__UDP__IFACE`     |Space-separated local IPs (16 LSB set to node-ID)  |`127.9.0.0 192.168.0.0`
Serial    |`uavcan.serial.iface`|`string`       |`UAVCAN__SERIAL__IFACE`  |Space-separated serial port names                  |`COM9 socket://127.0.0.1:50905`
CAN       |`uavcan.can.iface`   |`string`       |`UAVCAN__CAN__IFACE`     |Space-separated CAN iface names                    |`socketcan:vcan0 pcan:PCAN_USBBUS1`
CAN       |`uavcan.can.mtu`     |`natural16[1]` |`UAVCAN__CAN__MTU`       |Maximum transmission unit; selects Classic/FD      |`64`
CAN       |`uavcan.can.bitrate` |`natural32[2]` |`UAVCAN__CAN__BITRATE`   |Arbitration/data segment bits per second           |`1000000 4000000`
Loopback  |`uavcan.loopback`    |`bit[1]`       |`UAVCAN__LOOPBACK`       |Use loopback interface (only for basic testing)    |`1`

### Subscribing to subjects

`uavcan.si.unit.angle.Scalar.1.0` 타입의 subject 33을 subscribe는 아래와 같다;
데이터 타입 이름(data type name) 전에 subject-ID를 지정하는 방법을 보자.
이 subject에 대한 publisher가 있다면 출력을 보자.(다음 섹션에서 추가로 다룬다)

```bash
$ export UAVCAN__UDP__IFACE=127.63.0.0
$ yakut sub 33:uavcan.si.unit.angle.Scalar.1.0
---
33:
  _metadata_:
    timestamp: {system: 1608987583.298886, monotonic: 788272.540747}
    priority: nominal
    transfer_id: 0
    source_node_id: 42
  radian: 2.309999942779541

---
33:
  _metadata_:
    timestamp: {system: 1608987583.298886, monotonic: 788272.540747}
    priority: nominal
    transfer_id: 1
    source_node_id: 42
  radian: 2.309999942779541
```

### Publishing messages

2개 메시지를 동시에 2번 publish(총 4개 메시지):

```bash
export UAVCAN__UDP__IFACE=127.63.0.0
export UAVCAN__NODE__ID=42
yakut pub -N2 33:uavcan.si.unit.angle.Scalar.1.0 'radian: 2.31' \
                 uavcan.diagnostic.Record.1.1    'text: "2.31 rad"'
```

2번째 subject를 위해서 subject-ID를 지정하지 않았지만 고정된 subject-ID가 기본이 된다.

위 예제에서 쓸모없는 일정한 값을 publish한다.
publish하기 전에 Yakut가 수행하는 임의의 Python 코드를 정의할 수 있다.
이런 expression들은 [YAML tag](https://yaml.org/spec/1.2/spec.html#id2761292) `!$` 로 마킹된 문자열로 들어가 있다.
YAML 문서에는 임의 개수의 expression들이 있을 수 있고 결과적으로 마지막 구조체가 지정한 메시지로 초기화하고 결과는 임의의 값이 된다.
다음 예제는 1Hz 주기, 10 미터 진폭의 싸인파를 publish한다.:

```bash
yakut pub -T 0.01 1234:uavcan.si.unit.length.Scalar.1.0 '{meter: !$ "sin(t * pi * 2) * 10"}'
```

변수 `t`와 같은 엔트티를 사용하거나 expression에서 표준 `sin` 함수를 사용한다.
`yakut pub --help`를 사용하면 유효한 엔트티의 전체 목록을 보도록 하자.

이 명령의 특별한 기능은 연결된 조이스틱이나 MIDI 제어기로부터 데이터를 읽을 수 있다는 것이다.
사용자가 UAVCAN 프로세스나 장치를 실시간으로 제어할 수 있게 한다.
함수 `A(x,y)`는 연결된 제어기 `x`로부터 축 `y`의 normalized 값을 반환한다.(상세한 내용은 `yakut pub --help` 참고) 유사하게 push 버튼은 `B(x,y)` 이고 toggle 스위치는 `T(x,y)`이다.
다음 예제는 3D 각속도 setpoint, thrust setpoint, arming 스위치 상태를 publish하여 사용자가 상호작용으로 이 파라미터를 제어할 수 있게 한다.:

```bash
yakut pub -T 0.1 \
    5:uavcan.si.unit.angular_velocity.Vector3.1.0 'radian_per_second: !$ "[A(1,0)*10, A(1,1)*10, (A(1,2)-A(1,5))*5]"' \
    6:uavcan.si.unit.power.Scalar.1.0 'watt: !$ A(2,10)*1e3' \
    7:uavcan.primitive.scalar.Bit.1.0 'value: !$ T(1,5)'
```

연결된 제어기의 목록과 그 축들의 매핑은 `yakut joystick`를 사용해서 볼 수 있다. 아래 비디오 참고:

[![yakut joystick](https://img.youtube.com/vi/YPr98KM1RFM/maxresdefault.jpg)](https://www.youtube.com/watch?v=YPr98KM1RFM)


MIDI 제어기 예제는 사인파의 주파수와 진폭을 변경하는 예제이다.:

[![yakut publish](https://img.youtube.com/vi/DSsI882ZYh0/maxresdefault.jpg)](https://www.youtube.com/watch?v=DSsI882ZYh0)

### Invoking RPC-services

custom 데이터 타입이 주어지면:

```shell
# sirius_cyber_corp.PerformLinearLeastSquaresFit.1.0
PointXY.1.0[<64] points
@extent 1024 * 8
---
float64 slope
float64 y_intercept
@sealed
```

```shell
# sirius_cyber_corp.PointXY.1.0
float16 x
float16 y
@sealed
```

service-ID 123에 `sirius_cyber_corp.PerformLinearLeastSquaresFit.1.0`를 제공하는 node 42가 있다고 가정한다.:

```bash
$ export UAVCAN__UDP__IFACE=127.63.0.0
$ export UAVCAN__NODE__ID=42
$ yakut compile sirius_cyber_corp
$ yakut call 42 123:sirius_cyber_corp.PerformLinearLeastSquaresFit.1.0 'points: [{x: 10, y: 1}, {x: 20, y: 2}]'
---
123:
  slope: 0.1
  y_intercept: 0.0
```

## Monitoring the network

`yakut monitor` 명령은 네트워크 상에 있는 모든 동작을 간략히 표시할때 사용한다.
연결된 노드를 추적하고 네트워크 상에 각 노드들 사이에 교환되는 모든 전송을 실시간 통계를 구한다.
좀비 노드와 같은 일반적인 네트워크 설정 문제를 검출하는데 사용할 수도 있다.(`uavcan.node.Heartbeat`를 publish하지 않는 노드들)

상세한 내용은 `yakut monitor --help` 참고.

```bash
$ export UAVCAN__CAN__IFACE="socketcan:can0 socketcan:can1 socketcan:can2"  # Triply-redundant UAVCAN/CAN
$ export UAVCAN__CAN__MTU=8                     # Force MTU = 8 bytes
$ export UAVCAN__CAN__BITRATE="1000000 1000000" # Disable BRS, use the same bit rate for arbitration/data
$ y mon                                         # Abbreviation of "yakut monitor"
```

<img src="/docs/monitor.gif" alt="yakut monitor">

모니터는 익명 노드이거나 자신에게 node-ID를 부여할 수 있다.
후자의 경우 표준 회고 서비스를 사용해서 적극적으로 다른 노드들에게 쿼리를 날린다.

일부 트랜스포트들 그중에서 특히 UAVCAN/UDP는 이 도구를 실행시키기 위해서 특별한 권한이 필요하다. 이유는 low-level 패킷을 캡쳐를 위한 보안 때문이다.

## Updating node software

파일 서버 명령은 파일을 제공, PnP node-ID 할당 실행(일부 임베디드 bootloader 구현이 필요), 자동으로 sw 업데이트 요청 `uavcan.node.ExecuteCommand`를 노드들에게 전송한다.

이런 기능을 보여주기 위해 네트워크는 다음과 같은 노드들을 포함하고 있다고 가정한다:

- nodes 1, 2 named `com.example.foo`, software 1.0
- nodes 3, 4 named `com.example.bar`, hardware v4.2, software v3.4
- node 5 named `com.example.baz`

SW 업데이트는 atomic package 파일처럼 배포된다.
임베디드 시스템의 경우 이런 패키지는 보통 펌웨어 이미지이고 압축되거나 일부 메타데이터를 가질 수도 있다.
파일 서버가 파일 내부를 들여다 보지 않기 떄문에 파일 서버와는 무관하다.
하지만 파일 이름은 해당 파일의 패턴에 따라서 서버가 인지할 수 있게 만들 수 있으므로 
하지만 sw 패키지가 가지는 이름은 특정 패턴을 따라서 서버가 파일을 인지하도록 만들 수 있다.
명령 help로 전체 스펙 확인 : `yakut file-server --help`

배포할 패키지가 다음과 같다고 가정:

- v1.1 for nodes `com.example.foo` with any hardware
- v3.3 for nodes `com.example.bar` with hardware v4.x
- v3.5 for nodes `com.example.bar` with hardware v5.6 only
- nothing for `com.example.baz`

```shell
$ ls *.app*                       # List all software packages
com.example.foo-1.1.app.zip       # Any hardware
com.example.bar-4-3.3.app.pkg     # Hardware v4.x
com.example.bar-5.6-3.5.app.bin   # Hardware v5.6 only
```

새로운 노드가 네트워크에 발견되면 서버는 root 디렉토리를 스캔한다. 이 말은 런타임에 해당 패키지가 추가/삭제되고 서버는 비행중에 변경을 받아들일 수 있다.
서버 실행:

```shell
$ export UAVCAN__UDP__IFACE=127.63.0.0
$ export UAVCAN__NODE__ID=42
$ yakut file-server --plug-and-play=allocation_table.db --update-software
```

어떤 노드가 네트워크에 추가되면 서버는 `uavcan.node.GetInfo` 를 보내서 각 버전을 체크한다. 만약 새로운 패키지가 유효하면 해당 노드에게 `uavcan.node.ExecuteCommand`를 보내서 설치요청을 할 수 있다.

이런 특수한 경우에 다음이 발생한다:

- Nodes 1와 2가 v1.1로 업데이트된다.
- Nodes 3과 4는 업데이트 되지 않는다. 왜냐하면 새로운 패키지 v3.5는 하드웨어 v4.2와 호환되지 않고 호환 버전인 v3.3은 너무 오래된 버전이다.
- Node 5는 업데이트 되지 않는다. 왜냐하면 적절한 패키지가 없다.

`--verbose`를 추가하여 정확하게 결정이 어떻게 내려졌는지 확인한다.

이 명령은 **automatic network-wide configuration management**를 실행하기 위해서 사용할 수 있다.
서버를 시작하고 실행된 상태로 남겨둔다.
모든 관련 패키지를 루트 디렉토리로 저장한다.
노드가 연결되고 재시작되면 서버는 자동으로 로컬 파일과 업데이트를 수행할 파일의 버전을 비교한다.
따라서 전체 네트워크는 자동으로 최신으로 유지될 수 있다.