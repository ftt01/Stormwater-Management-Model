//-----------------------------------------------------------------------------
//   consts.h
//
//   Project: EPA SWMM5
//   Version: 5.1
//   Date:    03/20/14  (Build 5.1.001)
//   Author:  L. Rossman
//
//   Various Constants
//-----------------------------------------------------------------------------

//------------------
// General Constants
//------------------

#define   VERSION            51000
#define   MAGICNUMBER        516114522      //? Is it a fixed random number
#define   EOFMARK            0x1A           // Use 0x04 for UNIX systems
#define   MAXTITLE           3              // Max. # title lines
#define   MAXMSG             1024           // Max. # characters in message text
#define   MAXLINE            1024           // Max. # characters per input line
#define   MAXFNAME           259            // Max. # characters in file name
#define   MAXTOKS            40             // Max. items per line of input
#define   MAXSTATES          10             // Max. # computed hyd. variables
#define   MAXODES            4              // Max. # ODE's to be solved
#define   NA                 -1             // NOT APPLICABLE code
#define   TRUE               1              // Value for TRUE state
#define   FALSE              0 		    // Value for FALSE state
#define   BIG                1.E10          // Generic large value
#define   TINY               1.E-6          // Generic small value
#define   ZERO               1.E-10         // Effective zero value
#define   MISSING            -1.E10         // Missing value code
#define   PI                 3.141592654    // Value of pi
#define   GRAVITY            32.2           // accel. of gravity in US units
#define   SI_GRAVITY         9.81           // accel of gravity in SI units
#define   MAXFILESIZE        2147483647L    // largest file size in bytes

//-----------------------------
// Units factor in Manning Eqn.
//-----------------------------
#define   PHI 1.486

//----------------------------------------------
// Definition of measureable runoff flow & depth
//----------------------------------------------
#define   MIN_RUNOFF_FLOW    0.001          // cfs (cubic feet per second)
#define   MIN_EXCESS_DEPTH   0.0001         // ft, = 0.03 mm  <NOT USED>
#define   MIN_TOTAL_DEPTH    0.004167       // ft, = 0.05 inches
#define   MIN_RUNOFF         2.31481e-8     // ft/sec = 0.001 in/hr

//----------------------------------------------------------------------
// Minimum flow, depth & volume used to evaluate steady state conditions
//----------------------------------------------------------------------
#define   FLOW_TOL      0.00001  // ft^3/s
#define   DEPTH_TOL     0.00001  // ft    <NOT USED>
#define   VOLUME_TOL    0.01     // ft^3   <NOT USED>

//---------------------------------------------------
// Minimum depth for reporting non-zero water quality
//---------------------------------------------------
//#define   MIN_WQ_DEPTH  0.01     // ft (= 3 mm)
//#define   MIN_WQ_FLOW   0.001    // cfs

//-----------------------------------------------------
// Minimum flow depth and area for dynamic wave routing
//-----------------------------------------------------
#define   FUDGE    0.0001    // ft or ft^2

//---------------------------
// Various conversion factors
//---------------------------
#define   GPMperCFS   448.831	//! gallons per minute in a cubic feet per second
#define   AFDperCFS   1.9837  	//! acre-feet per day in a cubic feet per second
#define   MGDperCFS   0.64632 	//! million gallons per day in a cubic feet per second
#define   IMGDperCFS  0.5382	//! imperial gallons per day in a cubic feet per second
#define   LPSperCFS   28.317	//! liters per second in a cubic feet per second
#define   LPMperCFS   1699.0	//! liters per minute in a cubic feet per second
#define   CMHperCFS   101.94	//! cubic meters per hour in a cubic feet per second
#define   CMDperCFS   2446.6	//! cubic meters per day in a cubic feet per second
#define   MLDperCFS   2.4466	//! megaliters per day in a cubic feet per second
#define   M3perFT3    0.028317	//! cubic meters in a cubic feet
#define   LperFT3     28.317	//! liters in a cubic feet
#define   MperFT      0.3048	//! meters in a feet
#define   PSIperFT    0.4333	//! pound per square inch in a feet
#define   KPAperPSI   6.895	//! kilopascal in a pound per square inch
#define   KWperHP     0.7457	//! kilowatt in a horsepower
#define   SECperDAY   86400	//! seconds in a day
#define   MSECperDAY  8.64e7	//! milliseconds in a day
#define   MMperINCH   25.40	//! millimeters in an inch

//---------------------------
// Token separator characters
//--------------------------- 
#define   SEPSTR    " \t\n\r" 
