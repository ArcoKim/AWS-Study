# IPv4
## VPC
|Name|CIDR|Options|
|---|---|---|
|skills-vpc|10.0.0.0/16|Enable DNS resolution & Enable DNS hostnames|

## Subnets
|Name|CIDR|Options|
|---|---|---|
|skills-public-a|10.0.0.0/24|Enable auto-assign public IPv4 address|
|skills-public-c|10.0.1.0/24|Enable auto-assign public IPv4 address|
|skills-private-a|10.0.2.0/24||
|skills-private-c|10.0.3.0/24||
|skills-data-a|10.0.4.0/24||
|skills-data-c|10.0.5.0/24||

## Internet gateways
|Name|Attach|
|---|---|
|skills-igw|skills-vpc|

## NAT gateways
|Name|Subnet|
|---|---|
|skills-nat-a|skills-public-a|
|skills-nat-c|skills-public-c|

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
|10.0.0.0/16|local|

### Private
|Name|Subnet associations|
|---|---|
|skills-private-a-rt|skills-private-a|
|skills-private-c-rt|skills-private-c|

- private-a

|Destination|Target|
|---|---|
|0.0.0.0/0|skills-nat-a|
|10.0.0.0/16|local|

- private-c

|Destination|Target|
|---|---|
|0.0.0.0/0|skills-nat-c|
|10.0.0.0/16|local|

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