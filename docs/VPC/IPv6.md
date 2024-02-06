# IPv6
## VPC
|Name|IPv4 CIDR|IPv6 CIDR|Options|
|---|---|---|---|
|skills-vpc|10.0.0.0/16|Amazon-provided IPv6 CIDR block (2406:da12:f67:3800::/56)|Enable DNS resolution & Enable DNS hostnames|

## Subnets
|Name|IPv4 CIDR|IPv6 CIDR|Options|
|---|---|---|---|
|skills-public-a|10.0.0.0/24|2406:da12:f67:3800::/64|Enable auto-assign public IPv4 address|
|skills-public-c|10.0.1.0/24|2406:da12:f67:3801::/64|Enable auto-assign public IPv4 address|
|skills-private-a|10.0.2.0/24|2406:da12:f67:3802::/64||
|skills-private-c|10.0.3.0/24|2406:da12:f67:3803::/64||
|skills-data-a|10.0.4.0/24|2406:da12:f67:3804::/64||
|skills-data-c|10.0.5.0/24|2406:da12:f67:3805::/64||

## Internet gateways
|Name|Attach|
|---|---|
|skills-igw|skills-vpc|

## NAT gateways
|Name|Subnet|
|---|---|
|skills-nat-a|skills-public-a|
|skills-nat-c|skills-public-c|

## Egress only internet gateways
|Name|Attach|
|---|---|
|skills-eigw|skills-vpc|

## Route tables
### Public
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Subnet associations</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2" style="vertical-align : middle;text-align:center;">skills-public-rt</td>
            <td>skills-public-a</td>
        </tr>
        <tr>
            <td>skills-public-c</td>
        </tr>
    </tbody>
</table>

|Destination|Target|
|---|---|
|0.0.0.0/0|skills-igw|
|::/0|skills-igw|
|10.0.0.0/16|local|
|2406:da12:f67:3800::/56|local|

### Private
|Name|Subnet associations|
|---|---|
|skills-private-a-rt|skills-private-a|
|skills-private-c-rt|skills-private-c|

- private-a

|Destination|Target|
|---|---|
|0.0.0.0/0|skills-nat-a|
|::/0|skills-eigw|
|10.0.0.0/16|local|
|2406:da12:f67:3800::/56|local|

- private-c

|Destination|Target|
|---|---|
|0.0.0.0/0|skills-nat-c|
|::/0|skills-eigw|
|10.0.0.0/16|local|
|2406:da12:f67:3800::/56|local|

### Protected
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Subnet associations</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2" style="vertical-align : middle;text-align:center;">skills-data-rt</td>
            <td>skills-data-a</td>
        </tr>
        <tr>
            <td>skills-data-c</td>
        </tr>
    </tbody>
</table>

|Destination|Target|
|---|---|
|10.0.0.0/16|local|
|2406:da12:f67:3800::/56|local|