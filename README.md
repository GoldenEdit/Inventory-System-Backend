# Inventory-System-Backend

# Work on this locally:

1. Install Python
2. Clone this repo (fork it if you want to make some changes)
3. Setup venv (Virtual Enviroment)
   * `py -m pip install --user virtualenv`
   * Run `py -m venv venv` in the repo folder
     * Make sure not to commit any of your venv files if you make a commit!!!
   * Run `.\venv\Scripts\activate` in the repo folder to active venv
4. Install requirements from [requirements.txt](https://github.com/GoldenEdit/Inventory-System-Backend/blob/main/requirements.txt) (`pip install -r requirements.txt`)



# Database setup:

## Asset

Asset ID

Group ID - When present, asset is grouped into separate assets.

Allocation ID - Allocation to a person. Field cleared when asset is unallocated

Location ID - Where (can be roaming if taken by somebody)

Home ID - location where this should be when not in use

Barcode - only one code needs to be entered

Picture - store file location

RFID

QR Code

Asset Name - E.g. Lightstorm LS-300D

Asset Serial

Model ID

Asset Description

Manufacturer

Purchase Date

Disposal Date

Disposal Reason

Disposal Type ID

Location ID

Colour

Estimated Value

Purchase Supplier

Date Purchased

Warranty Details

High Value - Flag. True if asset is over £1k in value

Cannot Lend - Flag. True if asset cannot be loaned out

Asset Owner - Person ID

Asset Type ID

When items are grouped, individual items cannot be loaned but are checked in and out together. E.g. Aperture LS 300D would have light, yoke, power adapter, power cables, reflector, etc. System would flag person to check all going out.

## Group

Group ID

Group Name

Group Description

## Disposal Type

Disposal ID

Disposal Name - e.g. securely destroyed, sale, donation, sale, recycle

## Asset Type

Type ID

Type Name - e.g. camera, desk, chair

Type Description

## Location

Location ID

Location Name - e.g. AV shed 2

Location Area - e.g. MHS

## Allocations

Allocation ID

Person ID

Timestamp

Return Due Date

Returned Date

## People

Person ID

Person Name

Person Department

School - e.g. Belmont, Walker House

Lend - Flag. If false, person cannot be lent to

Staff - Flag. True if member of staff

RFID - enables RFID tap to take items out, etc

Barcode - enables barcode ID discovery (like RFID)

CanLogIn - If not true, this person cannot sign in to the system

Email - Possibly used as sign in ID, also could support SSO in the future

PasswordHash - Self explanatory 

IsAdmin - Admin users get extra permissions


## Group Item

Group Asset ID

Group ID

Item Name

Item Description

## Role

Role ID

TBA

## Audit Trail

Timestamp

User ID

Action Description

- Acts as a history//archive for all system changes. E.g. user changing email, item being taken out. This will enable a full history to be shown for a person, item, etc. This cannot link back to other tables as it will break rules of normalization. ID fields here should be static and not foreign keys. This may not be needed if SQL archiving can provide the same features – needs research.

## Stack

**Frontend:**

React: A popular JavaScript library for building user interfaces.

Redux: A predictable state management library that can be used with React to manage application state.

Axios: A library for making HTTP requests to interact with the backend API.

**Backend:**

Python & Flask

PostgreSQL: A powerful open-source relational database for storing the inventory data. (Temp using SQLite)


**Authentication:**

JSON Web Tokens (JWT): A standard for securely transmitting information between parties as JSON objects.

**Data Visualization:**

Chart.js: A JavaScript library for creating interactive and visually appealing charts.

**Hosting:**

Amazon Web Services (AWS), Microsoft Azure, OVH, AWS S3 / CloudFlare S3 / Wasabi S3: Cloud platforms for hosting the application, database and image storage.

All proxied through Cloudflare.

Need to discuss GDPR Compliance, Maybe host on school Network many security and access implications
