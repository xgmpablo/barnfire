'''
Andrew Till
Summer 2014

Materials class and example materials.
'''

#MINE
from directories import get_common_directories

#STDLIB
import os
import sys
import copy
sys.path.insert(1, get_common_directories()['nuclideData'])

#TPL
import numpy as np
import nuclide_data as nd
from iapws import IAPWS97 as steam

#MINE
from materials_util import calc_chord_length
import materials_util as util

###############################################################################
def get_materials_name2function_dict():
    return {
        # For CERT use
        'cert': get_cert_material,
        'certHpolyCfree': get_cert_Hpoly_Cfree,
        'certHh2o': get_cert_Hh2o,
        # For CASL use
        'CASLfuel': get_CASL_fuel_material,
        'CASLfuel_900K': get_CASL_fuel_material_900K,
        'CASLfuel_1200K': get_CASL_fuel_material_1200K,
        'CASLgas': get_CASL_gas_material,
        'CASLclad': get_CASL_cladding_material,
        'CASLmod': get_CASL_moderator_material,
        'CASLmod1B': get_CASL_moderator1B_material,
        'CASLmod2E': get_CASL_moderator2E_material,
        'CASLss': get_CASL_StainlessSteel_material,
        'CASLpyrex': get_CASL_pyrex_material,
        'CASLb4c': get_CASL_B4C_material,
        'CASLaic': get_CASL_AIC_material,
        # CASL Problem 4 (Page.54-55)
        'CASLfuel_P4_211': get_CASL_fuel_p4_211_material,
        'CASLfuel_P4_262': get_CASL_fuel_p4_262_material,
        'CASLmod_P4': get_CASL_moderator_p4_material,
        'CASLtopnozzle': get_CASL_topnozzle_material,
        'CASLbottomnozzle': get_CASL_bottomnozzle_material,
        'CASLcoreplates': get_CASL_coreplates_material,
        # CASL Problem 5 (Page.62 & 67)
        'CASLfuel_P5_31': get_CASL_fuel_p5_31_material,
        'CASLmod_P5': get_CASL_moderator_p5_material,
        'CASLpyrex_P5': get_CASL_pyrex_p5_material,
        'CASLb4c_P5': get_CASL_B4C_p5_material,
        'CASLaic_P5': get_CASL_AIC_p5_material,
        'CASLss_P5': get_CASL_StainlessSteel_p5_material,
        'CASLgas_P5': get_CASL_gas_p5_material,
        'CASLclad_P5': get_CASL_cladding_p5_material,


        # For 410 design use
        '410Design': get_410Design_material,
        # Simple examples
        'hpu': get_hpu_slurry_material,
        'hheu': get_hheu_slurry_material,
        'hleu': get_hleu_slurry_material,
        'puMetal': get_pu_metal_material,
        'puMetalHot': get_hot_pu_metal_material,
        'uMetal': get_u_metal_material,
        # Simple multi-temperature examples
        'uo2ColdPin': get_cold_pin_uo2_material,
        'uo2Cold': get_cold_uo2_material,
        'uo2InnerHot': get_inner_hot_uo2_material,
        'uo2MiddleHot': get_middle_hot_uo2_material,
        'uo2OuterHot': get_outer_hot_uo2_material,
        'moxCold': get_cold_mox_material,
        'moxInnerHot': get_inner_hot_mox_material,
        'moxMiddleHot': get_middle_hot_mox_material,
        'moxOuterHot': get_outer_hot_mox_material,
        'h2oCold': get_cold_h2o_material,
        'h2oHot': get_hot_h2o_material,
        'graphite': get_graphite_material,
        # C5G7
        'clowMOX': get_c5g7_low_mox_material,
        'cmedMOX': get_c5g7_med_mox_material,
        'chighMOX': get_c5g7_high_mox_material,
        'cUO2': get_c5g7_uo2_material,
        'cMOD': get_c5g7_moderator_material,
        'cGUIDE': get_c5g7_guide_tube_material,
        'cFCHAMBER': get_c5g7_fission_chamber_material,
        'cCR': get_c5g7_control_rod_material,
        # TRIGA (BOL)
        'tdFUEL': get_depleted_triga_fuel_material,
        'tdFUEL_0': get_depleted_triga_fuel_material_0,
        'tFUEL': get_triga_fuel_material,
        'tcFUEL': get_ctriga_fuel_material,
        'tZIRC': get_triga_zirconium_material,
        'tCLAD': get_triga_clad_material,
        'tcCLAD': get_ctriga_clad_material,
        'tMOD': get_triga_moderator_material,
        'tAIR': get_triga_air_material,
        'tGRIDPLATE': get_triga_grid_plate_material,
        'tGRAPHITE': get_triga_graphite_material,
        'tWATERGRAPHITE': get_triga_watergraphite_material,
        'tBORATEDGRAPHITE': get_triga_borated_graphite_material,
        'tB4C': get_triga_b4c_material,
        'tLEAD': get_triga_lead_material,
        #'tAIRTUBE': get_triga_air_tube_material,
        #'tIRRADIATIONTUBE': get_triga_irradiation_tube_material,
        # Iron (for time-dependent dissertation problem)
        'iron': get_iron_material,
        'thickiron': get_thick_iron_material,
        # Simplified PWR pincell (for Kord Smith)
        'kFUEL': get_kord_fuel_material,
        'kRFUEL': get_kord_rod_fuel_material,
        'kEFUEL': get_kord_enriched_fuel_material,
        'kCLAD': get_kord_clad_material,
        'kZR': get_kord_zirconium_material,
        'kMOD': get_kord_moderator_material,
        'kREFUEL': get_kord_enriched_rod_fuel_material,
        'kRMFUEL': get_kord_mox_rod_fuel_material,
        # UO2 (for Don Bruss)
        'debFUEL': get_bruss_enriched_rod_fuel_material,
        # Multi-temperature examples
        'mtH2O_0': get_multi_temperature_h2o_material_T0,
        'mtH2O_1': get_multi_temperature_h2o_material_T1,
        'mtH2O_2': get_multi_temperature_h2o_material_T2,
        'mtH2O_3': get_multi_temperature_h2o_material_T3,
        'mtH2O_4': get_multi_temperature_h2o_material_T4,
        'mtH2O_5': get_multi_temperature_h2o_material_T5,
        'mtH2O_6': get_multi_temperature_h2o_material_T6,
        'mtH2O_7': get_multi_temperature_h2o_material_T7,
        'mtH2O_8': get_multi_temperature_h2o_material_T8,
        'mtTFUEL_0': get_multi_temperature_triga_fuel_material_T0,
        'mtTFUEL_1': get_multi_temperature_triga_fuel_material_T1,
        'mtTFUEL_2': get_multi_temperature_triga_fuel_material_T2,
        'mtTFUEL_3': get_multi_temperature_triga_fuel_material_T3,
        'mtTFUEL_4': get_multi_temperature_triga_fuel_material_T4,
        'mtTFUEL_5': get_multi_temperature_triga_fuel_material_T5,
        'mtTFUEL_6': get_multi_temperature_triga_fuel_material_T6,
        'mtTFUEL_7': get_multi_temperature_triga_fuel_material_T7,
        'mtTGRAPHITE_0': get_multi_temperature_triga_graphite_material_T0,
        'mtTGRAPHITE_1': get_multi_temperature_triga_graphite_material_T1,
        'mtTGRAPHITE_2': get_multi_temperature_triga_graphite_material_T2,
        'mtTGRAPHITE_3': get_multi_temperature_triga_graphite_material_T3,
        'mtTGRAPHITE_4': get_multi_temperature_triga_graphite_material_T4,
        'mtTGRAPHITE_5': get_multi_temperature_triga_graphite_material_T5,
        'mtTGRAPHITE_6': get_multi_temperature_triga_graphite_material_T6,
        'mtTGRAPHITE_7': get_multi_temperature_triga_graphite_material_T7,
        'mtTGRAPHITE_8': get_multi_temperature_triga_graphite_material_T8,
        'mtTGRAPHITE_9': get_multi_temperature_triga_graphite_material_T9,
        'mtDTFUEL_0': get_multi_temperature_depleted_triga_fuel_material_T0,
        'mtDTFUEL_7': get_multi_temperature_depleted_triga_fuel_material_T7,
        'mtTB4C_0': get_multi_temperature_triga_b4c_material_T0,
        'mtTB4C_5': get_multi_temperature_triga_b4c_material_T5,
        'mtTB4C_7': get_multi_temperature_triga_b4c_material_T7,
    }

###############################################################################
def get_CASL_fuel_material():
    shortName = 'CASLfuel'
    longName = 'CASL fuel material'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:6.11864E-06, 235:7.18132E-04, 236:03.29861E-06, 238:2.21546E-02}
    elemAtomFracDict = {'O':4.57642E-02, 'U':2.28821E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_fuel_material_900K():
    shortName = 'CASLfuel_900K'
    longName = 'CASL fuel material at 900K'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 900. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:6.11864E-06, 235:7.18132E-04, 236:03.29861E-06, 238:2.21546E-02}
    elemAtomFracDict = {'O':4.57642E-02, 'U':2.28821E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_fuel_material_1200K():
    shortName = 'CASLfuel_1200K'
    longName = 'CASL fuel material at 1200K'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 1200. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:6.11864E-06, 235:7.18132E-04, 236:03.29861E-06, 238:2.21546E-02}
    elemAtomFracDict = {'O':4.57642E-02, 'U':2.28821E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_gas_material():
    shortName = 'CASLgas'
    longName = 'CASL gas material'
    atomDensity = 2.68714e-05
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    elemAtomFracDict = {'He':1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_cladding_material():
    shortName = 'CASLclad'
    longName = 'CASL cladding material'
    massDensity = 6.56 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    crAtomFractionsDict = {50:3.30121E-06, 52:6.36606E-05, 53:7.21860E-06, 54:1.79686E-06}
    feAtomFractionsDict = {54:8.68307E-06, 56:1.36306E-04, 57:3.14789E-06, 58:4.18926E-07}
    zrAtomFractionsDict = {90:2.18865E-02, 91:4.77292E-03, 92:7.29551E-03, 94:7.39335E-03, 
                           96:1.19110E-03}
    snAtomFractionsDict = {112:4.68066E-06, 114:3.18478E-06, 115:1.64064E-06, 116:7.01616E-05,
                           117:3.70592E-05, 118:1.16872E-04, 119:4.14504E-05, 120:1.57212E-04,
                           122:2.23417E-05, 124:2.79392E-05}
    hfAtomFractionsDict = {174:3.54138E-09, 176:1.16423E-07, 177:4.11686E-07, 178:6.03806E-07,
                           179:3.01460E-07, 180:7.76449E-07}
    elemAtomFracDict = {'Cr':7.59773E-05, 'Fe':1.48556E-04, 'Zr':4.25394E-02, 'Sn':4.82542E-04, 'Hf':2.21337E-06}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, zrAtomFractionsDict, 'Zr')
    override_abundances(ZAList, abundanceDict, snAtomFractionsDict, 'Sn')
    override_abundances(ZAList, abundanceDict, hfAtomFractionsDict, 'Hf')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_moderator_material():
    shortName = 'CASLmod'
    longName = 'CASL moderator material'
    massDensity = 0.743 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'h2o'
    bAtomFractionsDict = {10:1.07070E-05, 11:4.30971E-05}
    elemAtomFracDict = {'H':4.96224E-02, 'O':2.48112E-02, 'B':5.38041E-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_moderator2E_material():
    shortName = 'CASLmod2E'
    longName = 'CASL moderator 2E material'
    massDensity = 0.743 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'h2o'
    bAtomFractionsDict = {10:1.07070E-05, 11:4.30971E-05}
    elemAtomFracDict = {'H':4.96224E-02, 'O':2.48112E-02, 'B':5.38041E-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_moderator1B_material():
    shortName = 'CASLmod1B'
    longName = 'CASL moderator 1B material'
    massDensity = 0.661 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'h2o'
    bAtomFractionsDict = {10:9.52537E-06, 11:3.83408E-05}
    elemAtomFracDict = {'H':4.41459E-02, 'O':2.20729E-02, 'B':4.786617E-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_StainlessSteel_material():
    shortName = 'CASLss'
    longName = 'CASL stainless-steel material'
    massDensity = 8.0 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    siAtomFractionsDict = {28:1.58197E-03, 29:8.03653E-05, 30:5.30394E-05}
    crAtomFractionsDict = {50:7.64915E-04, 52:1.47506E-02, 53:1.67260E-03, 54:4.16346E-04}
    feAtomFractionsDict = {54:3.44776E-03, 56:5.41225E-02, 57:1.24992E-03, 58:1.66342E-04}
    niAtomFractionsDict = {58:5.30854E-03, 60:2.04484E-03, 61:8.88879E-05, 62:2.83413E-04, 64:7.21770E-05}
    elemAtomFracDict = {'C':3.20895E-04, 'Si':1.71537E-03, 'P':6.99938E-05, 'Cr':1.76045E-02, 'Mn':1.75387E-03, 'Fe':5.89865E-02, 'Ni':7.79786E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_pyrex_material():
    shortName = 'CASLpyrex'
    longName = 'CASL PYREX material'
    massDensity = 2.25 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    bAtomFractionsDict = {10:9.63266E-04, 11:3.90172E-03}
    siAtomFractionsDict = {28:1.81980E-02, 29:9.24474E-04, 30:6.10133E-04}
    elemAtomFracDict = {'B':4.86499E-03, 'O':4.67761E-02, 'Si':1.97326E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_B4C_material():
    shortName = 'CASLb4c'
    longName = 'CASL B4C material'
    atomDensity = 9.59100E-02 #1/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    bAtomFractionsDict = {10:1.52689E-02, 11:6.14591E-02}
    elemAtomFracDict = {'B':7.67280E-02, 'C':1.91820E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_AIC_material():
    shortName = 'CASLaic'
    longName = 'CASL AIC material'
    atomDensity = 5.38440718E-02 #1/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'free'
    agAtomFractionsDict = {107:2.36159E-02, 109:2.19403E-02}
    cdAtomFractionsDict = {106:3.41523E-05, 108:2.43165E-05, 110:3.41250E-04, 111:3.49720E-04, 112:6.59276E-04, 113:3.33873E-04, 114:7.84957E-04, 116:2.04641E-04}
    inAtomFractionsDict = {113:3.44262E-04, 115:7.68050E-03}
    elemAtomFracDict = {'Ag':2.19403E-02, 'Cd':2.631098E-04, 'In':8.024762E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, agAtomFractionsDict, 'Ag')
    override_abundances(ZAList, abundanceDict, cdAtomFractionsDict, 'Cd')
    override_abundances(ZAList, abundanceDict, inAtomFractionsDict, 'In')

    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_fuel_p4_211_material():
    shortName = 'CASLfuel_P4_211'
    longName = 'CASL fuel P4 211 material'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:4.04814E-06, 235:4.88801E-04, 236:2.23756E-06, 238:2.23844E-02}
    elemAtomFracDict = {'O':4.57591E-02, 'U':2.28794867E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_fuel_p4_262_material():
    shortName = 'CASLfuel_P4_262'
    longName = 'CASL fuel P4 262 material'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:5.09503E-06, 235:6.06733E-04, 236:2.76809E-06, 238:2.22663E-02}
    elemAtomFracDict = {'O':4.57617E-02, 'U':2.28808961E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_moderator_p4_material():
    shortName = 'CASLmod_P4'
    longName = 'CASL moderator p4 material'
    massDensity = 0.743 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'h2o'
    bAtomFractionsDict = {10:1.12012E-05, 11:4.50862E-05}
    elemAtomFracDict = {'H':4.96194E-02, 'O':2.48097E-02, 'B':5.62874E-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_topnozzle_material():
    shortName = 'CASLtopnozzle'
    longName = 'CASL top nozzle material'
    atomDensity = 7.71078E-02 #atom/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    hAtomFractionsDict  = {1:4.01187E-02}
    bAtomFractionsDict  = {10:9.05410E-06, 11:3.64439E-05}
    siAtomFractionsDict = {28:3.02920E-04, 29:1.53886E-05, 30:1.01561E-05}
    crAtomFractionsDict = {50:1.46468E-04, 52:2.82449E-03, 53:3.20275E-04, 54:7.97232E-05}
    feAtomFractionsDict = {54:6.60188E-04, 56:1.03635E-02, 57:2.39339E-04, 58:3.18517E-05}
    niAtomFractionsDict = {58:1.01650E-03, 60:3.91552E-04, 61:1.70205E-05, 62:5.42688E-05, 64:1.38207E-05}
    elemAtomFracDict = {'H':4.01187E-02, 'B':4.5498E-05, 'C':6.14459E-05, 'O':2.00593E-02, 'Si':3.28465E-04, 'P':1.34026E-05, 'Cr':3.3709562E-03, 'Mn':3.35836E-04, 'Fe':1.12949E-02, 'Ni':1.47934E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=atomDensity)
    return material

def get_CASL_bottomnozzle_material():
    shortName = 'CASLbottomnozzle'
    longName = 'CASL bottom nozzle material'
    atomDensity = 8.26822E-02 #atom/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    hAtomFractionsDict  = {1:3.57638E-02}
    bAtomFractionsDict  = {10:8.07351E-06, 11:3.24969E-05}
    siAtomFractionsDict = {28:4.41720E-04, 29:2.24397E-05, 30:1.48097E-05}
    crAtomFractionsDict = {50:2.13581E-04, 52:4.11869E-03, 53:4.67027E-04, 54:1.16253E-04}
    feAtomFractionsDict = {54:9.62690E-04, 56:1.51122E-02, 57:3.49006E-04, 58:4.64463E-05}
    niAtomFractionsDict = {58:1.48226E-03, 60:5.70964E-04, 61:2.48194E-05, 62:7.91351E-05, 64:2.01534E-05}
    elemAtomFracDict = {'H':4.01187E-02, 'B':4.05704E-05, 'C':8.96008E-05, 'O':1.78819E-02, 'Si':4.78969E-04, 'P':1.95438E-05, 'Cr':4.91555E-03, 'Mn':4.89719E-04, 'Fe':1.64703E-02, 'Ni':2.17733E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=atomDensity)
    return material

def get_CASL_coreplates_material():
    shortName = 'CASLcoreplates'
    longName = 'CASL core plates material'
    atomDensity = 7.97787E-02 #atom/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    hAtomFractionsDict  = {1:2.48098E-02}
    bAtomFractionsDict  = {10:5.62115E-06, 11:2.26258E-05}
    siAtomFractionsDict = {28:7.90985E-04, 29:4.01826E-05, 30:2.65197E-05}
    crAtomFractionsDict = {50:3.82458E-04, 52:7.37532E-03, 53:8.36302E-04, 54:2.08173E-04}
    feAtomFractionsDict = {54:1.72388E-03, 56:2.70613E-02, 57:6.24963E-04, 58:8.31710E-05}
    niAtomFractionsDict = {58:2.65427E-03, 60:1.02242E-03, 61:4.44439E-05, 62:1.41707E-04, 64:3.60885E-05}
    elemAtomFracDict = {'H':2.48098E-02, 'B':2.82470E-05, 'C':1.60447E-04, 'O':1.24049E-02, 'Si':8.57687E-04, 'P':3.49969E-05, 'Cr':7.96595E-03, 'Mn':8.76936E-04, 'Fe':2.87852E-02, 'Ni':3.85449E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=atomDensity)
    return material

def get_CASL_fuel_p5_31_material():
    shortName = 'CASLfuel_P5_31'
    longName = 'CASL fuel P5 material'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {234:6.11864E-06, 235:7.18132E-04, 236:03.29861E-06, 238:2.21546E-02}
    elemAtomFracDict = {'O':4.57642E-02, 'U':2.28821E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_moderator_p5_material():
    shortName = 'CASLmod_P5'
    longName = 'CASL moderator P5 material'
    massDensity = 0.743 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'h2o'
    bAtomFractionsDict = {10:1.06329E-05, 11:4.27988E-05}
    elemAtomFracDict = {'H':4.96228E-02, 'O':2.48114E-02, 'B':5.34317E-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_pyrex_p5_material():
    shortName = 'CASLpyrex_P5'
    longName = 'CASL PYREX P5 material'
    massDensity = 2.25 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    bAtomFractionsDict = {10:9.61468E-04, 11:3.89444E-03}
    siAtomFractionsDict = {28:1.81641E-02, 29:9.22749E-04, 30:6.08994E-04}
    elemAtomFracDict = {'B':4.85591E-03, 'O':4.66888E-02, 'Si':1.96958E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_StainlessSteel_p5_material():
    shortName = 'CASLss_P5'
    longName = 'CASL stainless-steel P5 material'
    massDensity = 8.0 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    siAtomFractionsDict = {28:1.58197E-03, 29:8.03653E-05, 30:5.30394E-05}
    crAtomFractionsDict = {50:7.64915E-04, 52:1.47506E-02, 53:1.67260E-03, 54:4.16346E-04}
    feAtomFractionsDict = {54:3.44776E-03, 56:5.41225E-02, 57:1.24992E-03, 58:1.66342E-04}
    niAtomFractionsDict = {58:5.30854E-03, 60:2.04484E-03, 61:8.88879E-05, 62:2.83413E-04, 64:7.21770E-05}
    elemAtomFracDict = {'C':3.20895E-04, 'Si':1.71537E-03, 'P':6.99938E-05, 'Cr':1.76045E-02, 'Mn':1.75387E-03, 'Fe':5.89865E-02, 'Ni':7.79786E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_CASL_B4C_p5_material():
    shortName = 'CASLb4c_P5'
    longName = 'CASL B4C P5 material'
    atomDensity = 9.59100E-02 #1/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    bAtomFractionsDict = {10:1.52689E-02, 11:6.14591E-02}
    elemAtomFracDict = {'B':7.67280E-02, 'C':1.91820E-02}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_AIC_p5_material():
    shortName = 'CASLaic_P5'
    longName = 'CASL AIC P5 material'
    atomDensity = 5.38440718E-02 #1/barn-cm
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    agAtomFractionsDict = {107:2.36159E-02, 109:2.19403E-02}
    cdAtomFractionsDict = {106:3.41523E-05, 108:2.43165E-05, 110:3.41250E-04, 111:3.49720E-04, 112:6.59276E-04, 113:3.33873E-04, 114:7.84957E-04, 116:2.04641E-04}
    inAtomFractionsDict = {113:3.44262E-04, 115:7.68050E-03}
    elemAtomFracDict = {'Ag':2.19403E-02, 'Cd':2.631098E-04, 'In':8.024762E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, agAtomFractionsDict, 'Ag')
    override_abundances(ZAList, abundanceDict, cdAtomFractionsDict, 'Cd')
    override_abundances(ZAList, abundanceDict, inAtomFractionsDict, 'In')

    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_gas_p5_material():
    shortName = 'CASLgas_P5'
    longName = 'CASL gas P5 material'
    atomDensity = 2.68714e-05
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    elemAtomFracDict = {'He':1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_CASL_cladding_p5_material():
    shortName = 'CASLclad_P5'
    longName = 'CASL cladding P5 material'
    massDensity = 6.56 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 565. #K
    thermalOpt = 'free'
    crAtomFractionsDict = {50:3.30121E-06, 52:6.36606E-05, 53:7.21860E-06, 54:1.79686E-06}
    feAtomFractionsDict = {54:8.68307E-06, 56:1.36306E-04, 57:3.14789E-06, 58:4.18926E-07}
    zrAtomFractionsDict = {90:2.18865E-02, 91:4.77292E-03, 92:7.29551E-03, 94:7.39335E-03, 
                           96:1.19110E-03}
    snAtomFractionsDict = {112:4.68066E-06, 114:3.18478E-06, 115:1.64064E-06, 116:7.01616E-05,
                           117:3.70592E-05, 118:1.16872E-04, 119:4.14504E-05, 120:1.57212E-04,
                           122:2.23417E-05, 124:2.79392E-05}
    hfAtomFractionsDict = {174:3.54138E-09, 176:1.16423E-07, 177:4.11686E-07, 178:6.03806E-07,
                           179:3.01460E-07, 180:7.76449E-07}
    elemAtomFracDict = {'Cr':7.59773E-05, 'Fe':1.48556E-04, 'Zr':4.25394E-02, 'Sn':4.82542E-04, 'Hf':2.21337E-06}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, zrAtomFractionsDict, 'Zr')
    override_abundances(ZAList, abundanceDict, snAtomFractionsDict, 'Sn')
    override_abundances(ZAList, abundanceDict, hfAtomFractionsDict, 'Hf')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_410Design_material():
    shortName = '410Design'
    longName = '410 Design Project'
    massDensity = 10.257 #g/cc
    fuelRadius = 0.4096 #cm
    temperature = 600. #K
    thermalOpt = 'h2o'
    uAtomFractionsDict = {235:7.18132E-04, 238:03.29861E-06, 239:2.21546E-02}
    npAtomFractionsDict = {239:1.0}
    puAtomFractionsDict = {239:1.0}
    elemAtomFracDict = {'O':4.57642E-02, 'H': 9.15E-02, 'U':2.28821E-02, 'Np': 2.2E-04, 'Pu': 2.2E-03}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, npAtomFractionsDict, 'Np')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cert_material():
    shortName = 'cert'
    longName = 'CERT material'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 296. #K
    thermalOpt = 'graphite'
    hAtomFractionsDict = {1:1.0}
    bAtomFractionsDict = {10:0.5, 11:0.5}
    feAtomFractionsDict = {54:0.3, 56:0.3, 58:0.3}
    crAtomFractionsDict = {50:0.3, 52:0.3, 53:0.3}
    niAtomFractionsDict = {58:0.3, 60:0.3, 61:0.2, 62:0.2, 64:0.2}
    amAtomFractionsDict = {241:1.0}
    elemAtomFracDict = {'H':4.0, 'C':1.0, 'O':1.0, 'N':1.0, 'B':1.0, 'Ar':1.0, 'Al':1.0, 'Fe': 1.0, 'F':1.0, 'Am':1.0, 'Be':1.0, 'Cr':1.0, 'Ni':1.0, 'Mn':1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni')
    override_abundances(ZAList, abundanceDict, amAtomFractionsDict, 'Am')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cert_Hpoly_Cfree():
    shortName = 'certHpolyCfree'
    longName = 'CERT H-poly Carbon-Free'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 296. #K
    thermalOpt = 'poly'
    hAtomFractionsDict = {1:1.0}
    elemAtomFracDict = {'H':4.0, 'C':1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cert_Hh2o():
    shortName = 'certHh2o'
    longName = 'CERT H-h2o'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    hAtomFractionsDict = {1:1.0}
    elemAtomFracDict = {'H':4.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_hpu_slurry_material():
    shortName = 'hpu'
    longName = 'Pu-H slurry'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 301. #K
    thermalOpt = 'free'
    puAtomFractionsDict = {239: 1.0}
    elemAtomFracDict = {'Pu': 0.07, 'H': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_hheu_slurry_material():
    shortName = 'hheu'
    longName = 'HEU-H slurry'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 301. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {235: 1.0}
    elemAtomFracDict = {'U': 0.07, 'H': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_hleu_slurry_material():
    shortName = 'hleu'
    longName = 'LEU-H slurry'
    massDensity = 5. #g/cc
    fuelRadius = 0. #cm
    temperature = 301. #K
    thermalOpt = 'free'
    uAtomFractionsDict = {235: 0.07, 238: 0.93}
    elemAtomFracDict = {'U': 1.0, 'H': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_pu_metal_material():
    shortName = 'Pu metal'
    longName = 'Pu metal'
    massDensity = 19.8 #g/cc
    fuelRadius = 0.0 #cm
    temperature = 301. #K
    thermalOpt = 'none'
    puAtomFractionsDict = {239: 1.0}
    elemAtomFracDict = {'Pu': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_hot_pu_metal_material(T=400.):
    material = get_pu_metal_material()
    material.update_temperature(T)
    material.update_names('puMetalHot', 'hot Pu metal')
    return material

def get_u_metal_material():
    shortName = 'U metal'
    longName = 'U metal'
    massDensity = 19.1 #g/cc
    fuelRadius = 0.0 #cm
    temperature = 301. #K
    thermalOpt = 'none'
    uAtomFractionsDict = {235: 0.05, 238: 0.95}
    elemAtomFracDict = {'U': 1}
    #
    chordLength = util.calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_uo2_material():
    shortName = 'UO2'
    longName = 'uranium dioxide'
    massDensity = 10.97 #g/cc
    fuelRadius = 0.47 #cm
    #fuelRadius = 0.0 #cm
    temperature = 301. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {235: 0.05, 238: 0.95}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cold_pin_uo2_material(T=400.):
    material = get_uo2_material()
    material.update_temperature(T)
    #material.update_mass_density(material.massDensity / 1.1)
    material.update_names('uo2PinCold', 'cold uranium dioxide')
    return material

def get_cold_uo2_material(T=400.):
    material = get_uo2_material()
    material.update_temperature(T)
    material.update_names('uo2Cold', 'cold uranium dioxide')
    return material

def get_inner_hot_uo2_material(T=1000.):
    material = get_uo2_material()
    material.update_temperature(T)
    material.update_names('uo2InnerHot', 'inner hot uranium dioxide')
    return material

def get_middle_hot_uo2_material(T=800.):
    material = get_uo2_material()
    material.update_temperature(T)
    material.update_names('uo2MiddleHot', 'middle hot uranium dioxide')
    return material

def get_outer_hot_uo2_material(T=700.):
    material = get_uo2_material()
    material.update_temperature(T)
    material.update_names('uo2OuterHot', 'outer hot uranium dioxide')
    return material

def get_mox_material():
    shortName = 'MOX'
    longName = 'mixed oxide'
    massDensity = 10.97 #g/cc
    fuelRadius = 0.47 #cm
    #fuelRadius = 0.0 #cm
    temperature = 301. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {238: 1.0}
    puAtomFractionsDict = {239: 1.0}
    elemAtomFracDict = {'O': 2, 'U': 0.95, 'Pu': 0.05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cold_mox_material(T=400.):
    material = get_mox_material()
    material.update_temperature(T)
    material.update_names('moxCold', 'cold mixed oxide')
    return material

def get_inner_hot_mox_material(T=1000.):
    material = get_mox_material()
    material.update_temperature(T)
    material.update_names('moxInnerHot', 'inner hot mixed oxide')
    return material

def get_middle_hot_mox_material(T=800.):
    material = get_mox_material()
    material.update_temperature(T)
    material.update_names('moxMiddleHot', 'middle hot mixed oxide')
    return material

def get_outer_hot_mox_material(T=700.):
    material = get_mox_material()
    material.update_temperature(T)
    material.update_names('moxOuterHot', 'outer hot mixed oxide')
    return material

def get_graphite_material():
    shortName = 'graphite'
    longName = 'graphite'
    massDensity = 1.72 #g/cc
    fuelRadius = 0.0 #cm
    temperature = 296. #K
    thermalOpt = 'graphite'
    elemAtomFracDict = {'C': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_thick_iron_material():
    shortName = 'thickiron'
    longName = 'thick iron'
    massDensity = 7.874 #g/cc
    fuelRadius = 1E-12 #cm (to give a large escape cross section)
    temperature = 296. #K
    thermalOpt = 'none'
    elemAtomFracDict = {'Fe': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_iron_material():
    shortName = 'iron'
    longName = 'iron'
    massDensity = 7.874 #g/cc
    # Unknown how I came about this:
    #fuelRadius = 13.41 #cm
    # Alternatively, we could use:
    #fuelRadius = 1E-12 #cm (make escape cross section large)
    # The iron reaction rate is proportional to (1-exp(-SigmaT*X)), where X is the iron thickness.
    # If we use SigmaEscape = 1/X, and our weighting spectrum is 1/(1+SigmaT*X),
    # then the energy shape of our iron reaction rate is (approximately):
    # SigmaT / (SigmaEscape + SigmaT) = SigmaT*X / (1 + SigmaT*X) ~= (1-exp(-SigmaT*X)).
    fuelRadius = 2.06 / 2 #cm (factor of 2 is to compensate for chord length being defined for cylinders)
    temperature = 296. #K
    thermalOpt = 'none'
    elemAtomFracDict = {'Fe': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material


def get_h2o_material():
    shortName = 'H2O'
    longName = 'light water'
    massDensity = 1.0 #g/cc
    fuelRadius = 0.47 #cm
    #fuelRadius = 0.0 #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    elemAtomFracDict = {'H': 2, 'O': 1}
    #
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    chordLength = calc_chord_length(fuelRadius)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_cold_h2o_material(T=400.):
    material = get_h2o_material()
    material.update_temperature(T)
    material.update_mass_density(0.749)
    material.update_names('h2oCold', 'cold light water')
    return material

def get_hot_h2o_material(T=550.):
    material = get_h2o_material()
    material.update_temperature(T)
    material.update_mass_density(0.749)
    material.update_names('h2oHot', 'hot light water')
    return material

def get_general_cold_h2o_material(T=293.6, P=0.1):
    #P in MPa, T in K, rho in g/cc
    rho = steam(P=P, T=T).rho / 1000
    material = get_h2o_material()
    material.update_temperature(T)
    material.update_mass_density(rho)
    material.update_chord_length(0.)
    material.update_names('h2oAtmCold', 'cold light water at atmospheric pressure')
    return material

def get_general_hot_h2o_material(T=570., P=15.5):
    #T: 275 - 315 C => 548 - 588 K
    #P in MPa, T in K, rho in g/cc
    rho = steam(P=P, T=T).rho / 1000
    material = get_h2o_material()
    material.update_temperature(T)
    material.update_mass_density(rho)
    material.update_chord_length(0.)
    material.update_names('h2oRxtHot', 'hot light water at high pressure')
    return material

###############################################################################
def get_c5g7_low_mox_material():
    shortName = 'clowMOX'
    longName = 'homogenized 4.3% MOX'
    atomDensity = 5.90443E-2
    fuelRadius = 0.54 #cm
    temperature = 296. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {235: 2.25734E-03, 238: 9.97743E-01}
    puAtomFractionsDict = {238: 1.51976E-02, 239: 5.87640E-01, 240: 2.43161E-01, 241: 9.92908E-02, 242: 5.47113E-02}
    amAtomFractionsDict = {241: 1.}
    elemAtomFracDict = {'U': 0.21573257, 'Pu': 0.009613, 'Am': 0.00012662, 'O': 0.45094438, 'Zr': 0.12712441, 'Al': 0.19645902}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    override_abundances(ZAList, abundanceDict, amAtomFractionsDict, 'Am')
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_med_mox_material():
    shortName = 'cmedMOX'
    longName = 'homogenized 7.0% MOX'
    atomDensity = 5.93894E-02
    fuelRadius = 0.54 #cm
    temperature = 296. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {235: 2.25734E-03, 238: 9.97743E-01}
    puAtomFractionsDict = {238: 1.51899E-02, 239: 5.88608E-01, 240: 2.46836E-01, 241: 9.62026E-02, 242: 5.31646E-02}
    amAtomFractionsDict = {241: 1.}
    elemAtomFracDict = {'U': 0.2144792, 'Pu': 0.01529919, 'Am': 0.00019366, 'O': 0.44832447, 'Zr': 0.12638584, 'Al': 0.19531763}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    override_abundances(ZAList, abundanceDict, amAtomFractionsDict, 'Am')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_high_mox_material():
    shortName = 'chighMOX'
    longName = 'homogenized 8.7% MOX'
    atomDensity = 5.96194E-02
    fuelRadius = 0.54 #cm
    temperature = 296. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {235: 2.25734E-03, 238: 9.97743E-01}
    puAtomFractionsDict = {238: 1.51899E-02, 239: 5.87342E-01, 240: 2.48101E-01, 241: 9.62025E-02, 242: 5.31645E-02}
    amAtomFractionsDict = {241: 1.}
    elemAtomFracDict = {'U': 0.21365168, 'Pu': 0.01905021, 'Am': 0.00024114, 'O': 0.44659472, 'Zr': 0.12589821, 'Al': 0.19456404}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    override_abundances(ZAList, abundanceDict, amAtomFractionsDict, 'Am')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_uo2_material():
    shortName = 'cUO2'
    longName = 'homogenized 3.7% UO2'
    atomDensity = 5.89782E-02
    fuelRadius = 0.54 #cm
    temperature = 296. #K
    thermalOpt = 'uo2'
    uAtomFractionsDict = {235: 3.74216E-02, 238: 9.62578E-01}
    elemAtomFracDict = {'U': 0.22538375, 'O': 0.45066999, 'Zr': 0.12726695, 'Al': 0.19667931}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_moderator_material():
    shortName = 'cMOD'
    longName = 'borated light water'
    atomDensity = 1.00528E-01
    fuelRadius = 0.54 #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    elemAtomFracDict = {'O': 0.33324115, 'H': 0.66648231, 'B': 2.765404E-04}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_guide_tube_material():
    shortName = 'cGUIDE'
    longName = 'homogenized guide tube'
    atomDensity = 7.60666E-02
    fuelRadius = 0.54 #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    elemAtomFracDict = {'O': 0.17459076, 'H':  0.34918152, 'B': 0.00014488, 'Al': 0.47608284}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_fission_chamber_material():
    shortName = 'cFCHAMBER'
    longName = 'homogenized fission chamber'
    atomDensity = 7.60666E-02
    fuelRadius = 0.54 #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    uAtomFractionsDict = {235: 1.0}
    elemAtomFracDict = {'U': 5.2117E-08, 'O': 0.174590749, 'H': 0.349181499, 'B': 0.000144884, 'Al': 0.476082816}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

def get_c5g7_control_rod_material():
    shortName = 'cCR'
    longName = 'homogenized control rod'
    atomDensity = 5.84389E-02
    fuelRadius = 0.54 #cm
    temperature = 293.6 #K
    thermalOpt = 'free'
    elemAtomFracDict = {'Al': 0.61969028, 'Ag': 0.30424777, 'In': 0.05704646, 'Cd': 0.01901549}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity)
    return material

###############################################################################
def get_depleted_triga_fuel_material():
    shortName = 'tcFUEL'
    longName = 'U-ZrH fuel w complete elems'
    massDensity = 7.03671478387 #g/cc
    fuelRadius = 1.7411 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'zrh'
 #   hAtomFractionsDict = {1: 0.999885, 2: 0.000115}
    uAtomFractionsDict = {234: 0.00237412107611, 235: 0.191509644035, 236: 0.00245944064973, 237: 9.38712924854e-08, 238: 0.803656700368, 239: 2.76322744152e-21}
    npAtomFractionsDict = {236: 4.87314780932e-07, 237: 0.98648993846, 238: 1.72038664926e-05, 239: 0.0134923703586}
    puAtomFractionsDict = {236: 1.06773890918e-12, 238: 0.000183915788017, 239: 0.97784115666, 240: 0.0205601536476, 241: 0.00140371098018, 242: 1.10629231985e-05, 243: 4.68515756757e-18}
    krAtomFractionsDict = {83: 1.0}
    moAtomFractionsDict = {95: 0.999628510895, 99: 0.000371489104873}
    tcAtomFractionsDict = {99: 1.0}
    ruAtomFractionsDict = {101: 1.0}
    rhAtomFractionsDict = {103: 0.999987416438, 105: 1.25835619908e-05}
    pdAtomFractionsDict = {105: 1.0}
    agAtomFractionsDict = {109: 1.0}
    cdAtomFractionsDict = {113: 1.0}
    iAtomFractionsDict = {129: 0.161950942944, 131: 0.00445235419208, 135: 0.833596702864}
    xeAtomFractionsDict = {131: 1.0}
    csAtomFractionsDict = {133: 0.350243510007, 134: 0.00113387916809, 135: 0.321648524355, 137: 0.32697408647}
    baAtomFractionsDict = {140: 1.0}
    laAtomFractionsDict = {139: 1.0}
    prAtomFractionsDict = {141: 1.0}
    ndAtomFractionsDict = {143: 0.592936443146, 145: 0.407063556854}
    pmAtomFractionsDict = {147: 0.998954629436, 148: 9.6327940823e-05, 149: 0.000126216870906, 548: 0.000822825752352}
    smAtomFractionsDict = {147: 0.331469151271, 149: 0.100586982076, 150: 0.308269138205, 151: 0.126675020028, 152: 0.132999708419}
    euAtomFractionsDict = {153: 0.876051566418, 154: 0.0174919650421, 155: 0.104649622945, 156: 0.00180684559459}
    gdAtomFractionsDict = {155: 0.796768926336, 157: 0.203231073664}
    erAtomFractionsDict = {162: 0.00137343144164, 164: 0.0159304392447, 166: 0.334071882669, 167: 0.199177751989, 168: 0.30050371386, 170: 0.148942780795}
    elemMassFracDict = {'U': 0.300040763497, 'Np': 5.51300952526e-06, 'Pu': 0.000358903274981, 'Kr': 3.44055902736e-06, 'Mo': 4.42040914636e-05, 'Tc': 4.74403500563e-05, 'Ru': 4.10396870386e-05, 'Rh': 2.38978004217e-05, 'Pd': 8.66313582917e-06, 'Ag': 3.51488451214e-07, 'Cd': 5.34122209673e-08, 'I': 3.52451301271e-05, 'Xe': 2.12993243475e-14, 'Cs': 0.000197945243164, 'Ba': 6.65278315976e-07, 'La': 7.03637701299e-05, 'Pr': 6.27897228019e-05, 'Nd': 0.000109340460356, 'Pm': 1.47672440039e-05, 'Sm': 3.12491981564e-05, 'Eu': 2.37042807623e-06, 'Gd': 7.48212729834e-08, 'Er': 0.00860558224939, 'Zr': 0.675063181105, 'H': 0.0115483336522, 'C': 0.00364500346199, 'Hf': 3.88179282427e-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemMassFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U', 'Mass')
    override_abundances(ZAList, abundanceDict, npAtomFractionsDict, 'Np', 'Mass')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu', 'Mass')
    override_abundances(ZAList, abundanceDict, krAtomFractionsDict, 'Kr', 'Mass')
    override_abundances(ZAList, abundanceDict, moAtomFractionsDict, 'Mo', 'Mass')
    override_abundances(ZAList, abundanceDict, tcAtomFractionsDict, 'Tc', 'Mass')
    override_abundances(ZAList, abundanceDict, ruAtomFractionsDict, 'Ru', 'Mass')
    override_abundances(ZAList, abundanceDict, rhAtomFractionsDict, 'Rh', 'Mass')
    override_abundances(ZAList, abundanceDict, pdAtomFractionsDict, 'Pd', 'Mass')
    override_abundances(ZAList, abundanceDict, agAtomFractionsDict, 'Ag', 'Mass')
    override_abundances(ZAList, abundanceDict, cdAtomFractionsDict, 'Cd', 'Mass')
    override_abundances(ZAList, abundanceDict, iAtomFractionsDict, 'I', 'Mass')
    override_abundances(ZAList, abundanceDict, xeAtomFractionsDict, 'Xe', 'Mass')
    override_abundances(ZAList, abundanceDict, csAtomFractionsDict, 'Cs', 'Mass')
    override_abundances(ZAList, abundanceDict, baAtomFractionsDict, 'Ba', 'Mass')
    override_abundances(ZAList, abundanceDict, laAtomFractionsDict, 'La', 'Mass')
    override_abundances(ZAList, abundanceDict, prAtomFractionsDict, 'Pr', 'Mass')
    override_abundances(ZAList, abundanceDict, ndAtomFractionsDict, 'Nd', 'Mass')
    override_abundances(ZAList, abundanceDict, pmAtomFractionsDict, 'Pm', 'Mass')
    override_abundances(ZAList, abundanceDict, smAtomFractionsDict, 'Sm', 'Mass')
    override_abundances(ZAList, abundanceDict, euAtomFractionsDict, 'Eu', 'Mass')
    override_abundances(ZAList, abundanceDict, gdAtomFractionsDict, 'Gd', 'Mass')
    override_abundances(ZAList, abundanceDict, erAtomFractionsDict, 'Er', 'Mass')
 #   override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemMassFracDict=elemMassFracDict, massDensity=massDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_depleted_triga_fuel_material_0():
    shortName = 'tcFUEL_0'
    longName = 'depleted U-ZrH fuel for group 0'
    massDensity = 7.03712243885 #g/cc
    fuelRadius = 1.7920 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'zrh'
    uAtomFractionsDict = {234: 0.00237593797953, 235: 0.191850538338, 236: 0.00235384419777, 237: 9.83570800426e-08, 238: 0.803419581128, 239: 7.34951899347e-21}
    npAtomFractionsDict = {236: 4.75175327858e-07, 237: 0.979359569485, 238: 1.72283981355e-05, 239: 0.0206227269414}
    puAtomFractionsDict = {236: 1.0165129505e-12, 238: 0.000179511452041, 239: 0.978492414475, 240: 0.0199418257917, 241: 0.00137463797917, 242: 1.16103012497e-05, 243: 4.96747661286e-18}
    krAtomFractionsDict = {83: 1.0}
    moAtomFractionsDict = {95: 0.999493460792, 99: 0.000506539208256}
    tcAtomFractionsDict = {99: 1.0}
    ruAtomFractionsDict = {101: 1.0}
    rhAtomFractionsDict = {103: 0.999983397462, 105: 1.6602537619e-05}
    pdAtomFractionsDict = {105: 1.0}
    agAtomFractionsDict = {109: 1.0}
    cdAtomFractionsDict = {113: 1.0}
    iAtomFractionsDict = {129: 0.161875969251, 131: 0.00492532303862, 135: 0.83319870771}
    xeAtomFractionsDict = {131: 1.0}
    csAtomFractionsDict = {133: 0.350006655089, 134: 0.00110074065573, 135: 0.321543868715, 137: 0.32734873554}
    baAtomFractionsDict = {140: 1.0}
    laAtomFractionsDict = {139: 1.0}
    prAtomFractionsDict = {141: 1.0}
    ndAtomFractionsDict = {143: 0.592721850187, 145: 0.407278149813}
    pmAtomFractionsDict = {147: 0.998887521779, 148: 9.94987831307e-05, 149: 0.000177085934389, 548: 0.000835893503465}
    smAtomFractionsDict = {147: 0.324637254037, 149: 0.10784358753, 150: 0.305104535025, 151: 0.128976472686, 152: 0.133438150722}
    euAtomFractionsDict = {153: 0.874416163934, 154: 0.0169891366143, 155: 0.106686050938, 156: 0.00190864851369}
    gdAtomFractionsDict = {155: 0.782267746745, 157: 0.217732253255}
    erAtomFractionsDict = {162: 0.00137598775175, 164: 0.0159425401897, 166: 0.334225123263, 167: 0.203765475762, 168: 0.295726872103, 170: 0.14896400093}
    elemMassFracDict = {'U': 0.577261099635, 'Np': 9.83066023567e-06, 'Pu': 0.000641010139292, 'Kr': 6.14038720784e-06, 'Mo': 7.83261923633e-05, 'Tc': 8.46397540944e-05, 'Ru': 7.32235072512e-05, 'Rh': 4.25306093512e-05, 'Pd': 1.54430692546e-05, 'Ag': 6.24461916685e-07, 'Cd': 9.90783178258e-08, 'I': 6.28971369797e-05, 'Xe': -3.39206680941e-14, 'Cs': 0.000353295367407, 'Ba': 1.28879873541e-06, 'La': 0.000125545820228, 'Pr': 0.000111782849074, 'Nd': 0.000195011942252, 'Pm': 2.69089775217e-05, 'Sm': 5.51941031766e-05, 'Eu': 4.23021088073e-06, 'Gd': 1.3253849464e-07, 'Er': 0.0182166597237, 'Zr': 1.28978397707, 'H': 0.0220643876356, 'C': 0.00696418823189, 'Hf': 7.41660088593e-05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemMassFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U', 'Mass')
    override_abundances(ZAList, abundanceDict, npAtomFractionsDict, 'Np', 'Mass')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu', 'Mass')
    override_abundances(ZAList, abundanceDict, krAtomFractionsDict, 'Kr', 'Mass')
    override_abundances(ZAList, abundanceDict, moAtomFractionsDict, 'Mo', 'Mass')
    override_abundances(ZAList, abundanceDict, tcAtomFractionsDict, 'Tc', 'Mass')
    override_abundances(ZAList, abundanceDict, ruAtomFractionsDict, 'Ru', 'Mass')
    override_abundances(ZAList, abundanceDict, rhAtomFractionsDict, 'Rh', 'Mass')
    override_abundances(ZAList, abundanceDict, pdAtomFractionsDict, 'Pd', 'Mass')
    override_abundances(ZAList, abundanceDict, agAtomFractionsDict, 'Ag', 'Mass')
    override_abundances(ZAList, abundanceDict, cdAtomFractionsDict, 'Cd', 'Mass')
    override_abundances(ZAList, abundanceDict, iAtomFractionsDict, 'I', 'Mass')
    override_abundances(ZAList, abundanceDict, xeAtomFractionsDict, 'Xe', 'Mass')
    override_abundances(ZAList, abundanceDict, csAtomFractionsDict, 'Cs', 'Mass')
    override_abundances(ZAList, abundanceDict, baAtomFractionsDict, 'Ba', 'Mass')
    override_abundances(ZAList, abundanceDict, laAtomFractionsDict, 'La', 'Mass')
    override_abundances(ZAList, abundanceDict, prAtomFractionsDict, 'Pr', 'Mass')
    override_abundances(ZAList, abundanceDict, ndAtomFractionsDict, 'Nd', 'Mass')
    override_abundances(ZAList, abundanceDict, pmAtomFractionsDict, 'Pm', 'Mass')
    override_abundances(ZAList, abundanceDict, smAtomFractionsDict, 'Sm', 'Mass')
    override_abundances(ZAList, abundanceDict, euAtomFractionsDict, 'Eu', 'Mass')
    override_abundances(ZAList, abundanceDict, gdAtomFractionsDict, 'Gd', 'Mass')
    override_abundances(ZAList, abundanceDict, erAtomFractionsDict, 'Er', 'Mass')
    override_abundances_as_elemental(ZAList, abundanceDict,  'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemMassFracDict=elemMassFracDict, massDensity=massDensity,
        temperatureIndex=temperatureIndex)
    return material
        
def get_triga_fuel_material():
    shortName = 'tFUEL'
    longName = 'U-ZrH fuel'
    atomDensity = 8.71115E-2
    fuelRadius = 1.7411 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'zrh'
    uAtomFractionsDict = {234: 0.000132187, 235: 0.017378221, 236: 0.000194346, 237: 1.0E-24, 238: 0.069406717}
    #npAtomFractionsDict = {237: 1.0E-24, 238: 1.0E-24, 239: 1.0E-24}
    #puAtomFractionsDict = {238: 1.0E-24, 239: 1.0E-24, 240: 1.0E-24, 241: 1.0E-24, 242: 1.0E-24}
    #amAtomFractionsDict = {241: 1.0E-24, 242: 1.0E-24, 243: 1.0E-24, 642: 1.0E-24}
    #cmAtomFractionsDict = {242: 1.0E-24, 243: 1.0E-24}
    #xeAtomFractionsDict = {135: 1.0E-24}
    #smAtomFractionsDict = {149: 1.0E-24}
    hAtomFractionsDict = {1: 0.999885, 2: 0.000115}
    #elemAtomFracDict = {'U': 0.062260112, 'Np': 1E-24, 'Pu': 1E-24, 'Am': 1E-24, 'Cm': 1E-24, 'Xe': 1E-24, 'Sm': 1E-24, 'Zr': 0.370555099, 'Hf': 2.22332E-05, 'Er': 0.002650567, 'C': 0.000205141, 'H': 0.564306848}
    elemAtomFracDict = {'U': 0.062260112, 'Zr': 0.370555099, 'Hf': 2.22332E-05, 'Er': 0.002650567, 'C': 0.000205141, 'H': 0.564306848}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #override_abundances(ZAList, abundanceDict, npAtomFractionsDict, 'Np')
    #override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #override_abundances(ZAList, abundanceDict, amAtomFractionsDict, 'Am')
    #override_abundances(ZAList, abundanceDict, cmAtomFractionsDict, 'Cm')
    #override_abundances(ZAList, abundanceDict, xeAtomFractionsDict, 'Xe')
    #override_abundances(ZAList, abundanceDict, smAtomFractionsDict, 'Sm')
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_ctriga_fuel_material():
    shortName = 'tcFUEL'
    longName = 'U-ZrH fuel complete'
    atomDensity = 8.71115E-2
    fuelRadius = 1.7411 - 0.3175 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'zrh'
    uAtomFractionsDict = {234: 9.44763913e-05, 235: 1.24205225e-02 , 236: 1.38902530e-04, 237: 7.14717721e-25, 238: 4.96062106e-02}
    hfAtomFractionsDict = {176: 1.16946632e-06, 177: 4.13537520e-06, 178: 6.06521696e-06, 179: 3.02816184e-06, 180: 7.81190561e-06}
    erAtomFractionsDict = {164: 4.24355777e-05, 166: 8.89255527e-04, 167:  6.06158167e-04, 168: 7.15069965e-04, 170: 3.95199540e-04}
    zrAtomFractionsDict = {90: 1.90650598e-01, 91: 4.15762821e-02, 92: 6.35501995e-02, 94: 6.44024762e-02, 96: 1.03755428e-02}
    hAtomFractionsDict = {1: 5.64241953e-01, 2: 6.48952875e-05}
    elemAtomFracDict = {'U': 6.22603E-02, 'Zr': 3.70556E-01, 'Hf': 2.22102E-05, 'Er': 2.64813E-03, 'C': 2.05142E-04, 'H': 5.64308E-01}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, hfAtomFractionsDict, 'Hf')
    override_abundances(ZAList, abundanceDict, erAtomFractionsDict, 'Er')
    override_abundances(ZAList, abundanceDict, zrAtomFractionsDict, 'Zr')
    override_abundances(ZAList, abundanceDict, hAtomFractionsDict, 'H')
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_clad_material():
    shortName = 'tCLAD'
    longName = 'SS304 clad'
    atomDensity = 8.58765E-02
    fuelRadius = 1.7920 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    elemAtomFracDict = {'Cr': 0.202441879, 'Fe': 0.687731801, 'Ni': 0.089657823, 'Mn': 0.020168498}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_ctriga_clad_material():
    shortName = 'tcCLAD'
    longName = 'SS304 clad complete'
    massDensity = 8.0
    fuelRadius = 1.7920 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    siAtomFractionsDict = {28: 0.004594, 29: 0.000241, 30: 0.000165}
    sAtomFractionsDict  = {32: 0.000142, 33: 0.000001, 34: 0.000007}
    crAtomFractionsDict = {50: 0.007930, 52: 0.159031, 53: 0.018378, 54: 0.004661}
    feAtomFractionsDict = {54: 0.039996, 56: 0.644764, 57: 0.015026, 58: 0.002039}
    niAtomFractionsDict = {58: 0.062340, 60: 0.024654, 60: 0.001085, 62: 0.003504, 64: 0.000917}
    elemMassFracDict = {'C': 0.0003, 'Si': 0.005, 'P': 0.000225, 'S': 0.00015, 'Cr': 0.19, 'Mn': 0.01, 'Fe': 0.701825, 'Ni': 0.0925}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemMassFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    override_abundances(ZAList, abundanceDict, siAtomFractionsDict, 'Si', 'Mass')
    override_abundances(ZAList, abundanceDict, sAtomFractionsDict, 'S', 'Mass')
    override_abundances(ZAList, abundanceDict, crAtomFractionsDict, 'Cr', 'Mass')
    override_abundances(ZAList, abundanceDict, feAtomFractionsDict, 'Fe', 'Mass')
    override_abundances(ZAList, abundanceDict, niAtomFractionsDict, 'Ni', 'Mass')

    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemMassFracDict=elemMassFracDict, massDensity=massDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_zirconium_material():
    shortName = 'tZIRC'
    longName = 'Zr fuel center'
    atomDensity =  0.01296
    fuelRadius = 0.3175 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    elemAtomFracDict = {'Zr': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_graphite_material():
    shortName = 'tGRAPHITE'
    longName = 'graphite'
    atomDensity = 8.52100E-02
    fuelRadius = 2.19255 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'graphite'
    elemAtomFracDict = {'C': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_borated_graphite_material():
    shortName = 'tBORATEDGRAPHITE'
    longName = 'borated graphite'
    atomDensity = 1.27794E-01
    fuelRadius = 1.7411 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'graphite'
    elemAtomFracDict = {'C': 0.788925928, 'B': 0.211074072}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_b4c_material():
    shortName = 'tB4C'
    longName = 'B4C powder'
    atomDensity = 1.35143E-01
    fuelRadius = 1.5164 #cm
    temperature = 296. #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    bAtomFractionsDict = {10: 0.020950, 11: 0.084310}
    elemAtomFracDict = {'C': 0.026320, 'B': 0.105260}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances_as_elemental(ZAList, abundanceDict, 'C')
    override_abundances(ZAList, abundanceDict, bAtomFractionsDict, 'B')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_irradiation_tube_material():
    shortName = 'tIRRADIATIONTUBE'
    longName = 'homogenized air-filled, Al-lined tube in water'
    atomDensity = 4.90539E-02
    fuelRadius = 2.19255 #cm
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'h2o'
    elemAtomFracDict = {'O': 0.29203693, 'H': 0.58387295, 'N': 0.00038432, 'Al': 0.12370580}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_moderator_material():
    shortName = 'tMOD'
    longName = 'light water'
    atomDensity = 0.09989 #1.00037E-1
    fuelRadius = 1.7920 #cm
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'h2o'
    elemAtomFracDict = {'O': 1.0, 'H': 2.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_air_tube_material():
    shortName = 'tAIRTUBE'
    longName = 'homogenized air-filled tube in water'
    atomDensity = 2.73966E-02
    fuelRadius = 3.8 #cm
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'h2o'
    elemAtomFracDict = {'O': 0.00017253, 'H': 0.00017253, 'N': 0.00017253}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_grid_plate_material():
    shortName = 'tGRIDPLATE'
    longName = 'structural Al'
    #massDensity = 2.7 # g/cc
    atomDensity = 0.059195 #a/b-cm
    fuelRadius = 10. #cm (complete guess)
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'al'
    #thermalOpt = 'free'
    elemAtomFracDict = {'Al': 0.058693, 'Fe': 0.000502}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_air_material():
    shortName = 'tAIR'
    longName = 'Air'
    atomDensity = 5.03509E-5
    fuelRadius = 'unshielded'
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    elemAtomFracDict = {'O': 0.2, 'N': 0.8}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, atomDensity=atomDensity,
        temperatureIndex=temperatureIndex)
    return material

def get_triga_lead_material():
    shortName = 'tLEAD'
    longName = 'lead'
    massDensity = 11.34 # g/cc
    fuelRadius = 10. #cm (complete guess)
    temperature = 293.6 #K
    temperatureIndex = 0 # X in .9Xc
    thermalOpt = 'free'
    elemAtomFracDict = {'Pb': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity,
        temperatureIndex=temperatureIndex)
    return material

###############################################################################
def get_bruss_enriched_rod_fuel_material():
    shortName = 'debFUEL'
    longName = 'uranium dioxide (rod)'
    massDensity = 10.29769 #g/cc
    fuelRadius = 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    temperature = 500 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 0.95, 235: 0.05}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

###############################################################################
def get_kord_fuel_material():
    shortName = 'kFUEL'
    longName = 'depleted uranium dioxide'
    massDensity = 10.29769 #g/cc
    MCNPfactor = 2.01692089627977
    fuelRadius = MCNPfactor * 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    #temperature = 296. #K
    #thermalOpt = 'uo2'
    temperature = 293.6 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 1.0}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_rod_fuel_material():
    shortName = 'kRFUEL'
    longName = 'depleted uranium dioxide (rod)'
    massDensity = 10.29769 #g/cc
    # In a 2D pin cell, the fuel is a cylinder/rod, not a slab, and a different chord length is used
    fuelRadius = 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    #temperature = 296. #K
    #thermalOpt = 'uo2'
    temperature = 293.6 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 1.0}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_enriched_rod_fuel_material():
    shortName = 'kREFUEL'
    longName = 'uranium dioxide (rod)'
    massDensity = 10.29769 #g/cc
    # In a 2D pin cell, the fuel is a cylinder/rod, not a slab, and a different chord length is used
    fuelRadius = 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    #temperature = 296. #K
    #thermalOpt = 'uo2'
    temperature = 293.6 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 0.96, 235: 0.04}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_mox_rod_fuel_material():
    shortName = 'kRMFUEL'
    longName = 'MOX (rod)'
    massDensity = 10.29769 #g/cc
    # In a 2D pin cell, the fuel is a cylinder/rod, not a slab, and a different chord length is used
    fuelRadius = 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    #temperature = 296. #K
    #thermalOpt = 'uo2'
    temperature = 293.6 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 1.0}
    puAtomFractionsDict = {239: 1.0}
    elemAtomFracDict = {'O': 2, 'U': 0.95, 'Pu': 0.05}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    override_abundances(ZAList, abundanceDict, puAtomFractionsDict, 'Pu')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_enriched_fuel_material():
    shortName = 'kEFUEL'
    longName = 'enriched uranium dioxide'
    massDensity = 10.29769 #g/cc
    MCNPfactor = 2.01692089627977
    fuelRadius = MCNPfactor * 0.39218 #cm
    # Want a consistent thermal behavior with MCNP
    #temperature = 296. #K
    #thermalOpt = 'uo2'
    temperature = 293.6 #K
    thermalOpt = 'free'
    uAtomFractionsDict = {238: 0.96, 235: 0.04}
    elemAtomFracDict = {'O': 2, 'U': 1}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    override_abundances(ZAList, abundanceDict, uAtomFractionsDict, 'U')
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_zirconium_material():
    shortName = 'kZR'
    longName = 'zirconium cladding'
    # This density is a homogenization of clad and void from an OpenMC pincell
    massDensity = 5.8105 #g/cc
    fuelRadius = 0.45720 #cm
    temperature = 293.6 #K
    thermalOpt = 'free'
    elemAtomFracDict = {'Zr': 1.0}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_clad_material():
    shortName = 'kCLAD'
    longName = 'zircaloy cladding'
    # This density is a homogenization of clad and void from an OpenMC pincell
    massDensity = 5.8105 #g/cc
    fuelRadius = 0.45720 #cm
    temperature = 293.6 #K
    thermalOpt = 'free'
    elemAtomFracDict = {'O': 0.0070946, 'Cr': 0.0017464, 'Fe': 0.0034148, 'Zr': 0.9766522, 'Sn': 0.011092}
    #
    chordLength = calc_chord_length(fuelRadius)
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_kord_moderator_material():
    material = get_h2o_material()
    material.update_temperature(293.6) #K
    material.update_mass_density(0.740582)
    material.update_names('kMOD', 'cold light water')
    return material

###############################################################################
def get_multi_temperature_h2o_material_base():
    shortName = 'mtH2O'
    longName = 'light water'
    massDensity = 1.0 #g/cc
    fuelRadius = 1.7920 #cm
    temperature = 293.6 #K
    thermalOpt = 'h2o'
    temperatureIndex = 0 # X in .9Xc
    # Hack to align thermal grids:
    #thermalOpt = 'free'
    elemAtomFracDict = {'H': 2, 'O': 1}
    #
    symDict, ZList, ZAList = get_all_isotopes(elemAtomFracDict)
    abundanceDict = lookup_natl_abundances(ZAList)
    chordLength = calc_chord_length(fuelRadius)
    #
    material = Material(
        shortName=shortName, longName=longName,
        temperature=temperature, thermalOpt=thermalOpt,
        symDict=symDict, ZList=ZList, ZAList=ZAList,
        abundanceDict=abundanceDict, chordLength=chordLength,
        elemAtomFracDict=elemAtomFracDict, massDensity=massDensity)
    return material

def get_multi_temperature_h2o_material_Tgrid():
    return [293.6, 350, 400, 450, 500, 550, 600, 650, 800] #K

def get_multi_temperature_h2o_material_Ti(iT):
    P = 0.101325 #MPa
    #P = 15.5 #MPa
    material = get_multi_temperature_h2o_material_base()
    Tgrid = get_multi_temperature_h2o_material_Tgrid()
    T = Tgrid[iT]
    rho = steam(P=P, T=T).rho / 1000
    shortName = 'mtH2O_{}'.format(iT)
    longName = 'light water ({} K)'.format(T)
    material.update_temperature(T)
    material.update_temperature_index(iT) # X in .9Xc
    material.update_mass_density(rho)
    material.update_names(shortName, longName)
    return material

def get_multi_temperature_h2o_material_T0():
    return get_multi_temperature_h2o_material_Ti(0)

def get_multi_temperature_h2o_material_T1():
    return get_multi_temperature_h2o_material_Ti(1)

def get_multi_temperature_h2o_material_T2():
    return get_multi_temperature_h2o_material_Ti(2)

def get_multi_temperature_h2o_material_T3():
    return get_multi_temperature_h2o_material_Ti(3)

def get_multi_temperature_h2o_material_T4():
    return get_multi_temperature_h2o_material_Ti(4)

def get_multi_temperature_h2o_material_T5():
    return get_multi_temperature_h2o_material_Ti(5)

def get_multi_temperature_h2o_material_T6():
    return get_multi_temperature_h2o_material_Ti(6)

def get_multi_temperature_h2o_material_T7():
    return get_multi_temperature_h2o_material_Ti(7)

def get_multi_temperature_h2o_material_T8():
    return get_multi_temperature_h2o_material_Ti(8)

###############################################################################
def get_multi_temperature_triga_fuel_material_base():
    return get_triga_fuel_material()

def get_multi_temperature_triga_fuel_material_Tgrid():
    return [296, 400, 500, 600, 700, 800, 1000, 1200] #K

def get_multi_temperature_triga_fuel_material_Ti(iT):
    material = get_multi_temperature_triga_fuel_material_base()
    Tgrid = get_multi_temperature_triga_fuel_material_Tgrid()
    T = Tgrid[iT]
    shortName = 'mtTFUEL_{}'.format(iT)
    longName = '{} ({} K)'.format(material.longName, T)
    material.update_temperature(T)
    material.update_temperature_index(iT) # X in .9Xc
    # MASS DENSITY SHOULD BE UPDATED TO ACCOUNT FOR THERMAL EXPANSION
    #material.update_mass_density(rho)
    material.update_names(shortName, longName)
    return material

def get_multi_temperature_triga_fuel_material_T0():
    return get_multi_temperature_triga_fuel_material_Ti(0)

def get_multi_temperature_triga_fuel_material_T1():
    return get_multi_temperature_triga_fuel_material_Ti(1)

def get_multi_temperature_triga_fuel_material_T2():
    return get_multi_temperature_triga_fuel_material_Ti(2)

def get_multi_temperature_triga_fuel_material_T3():
    return get_multi_temperature_triga_fuel_material_Ti(3)

def get_multi_temperature_triga_fuel_material_T4():
    return get_multi_temperature_triga_fuel_material_Ti(4)

def get_multi_temperature_triga_fuel_material_T5():
    return get_multi_temperature_triga_fuel_material_Ti(5)

def get_multi_temperature_triga_fuel_material_T6():
    return get_multi_temperature_triga_fuel_material_Ti(6)

def get_multi_temperature_triga_fuel_material_T7():
    return get_multi_temperature_triga_fuel_material_Ti(7)

###############################################################################
def get_multi_temperature_triga_graphite_material_base():
    return get_triga_graphite_material()

def get_multi_temperature_triga_graphite_material_Tgrid():
    return [296., 400., 500., 600., 700., 800., 1000., 1200., 1600., 2000.] #K

def get_multi_temperature_triga_graphite_material_Ti(iT):
    material = get_multi_temperature_triga_graphite_material_base()
    Tgrid = get_multi_temperature_triga_graphite_material_Tgrid()
    T = Tgrid[iT]
    shortName = 'mtTGRAPHITE_{}'.format(iT)
    longName = '{} ({} K)'.format(material.longName, T)
    material.update_temperature(T)
    material.update_temperature_index(iT) # X in .9Xc
    # MASS DENSITY SHOULD BE UPDATED TO ACCOUNT FOR THERMAL EXPANSION
    #material.update_mass_density(rho)
    material.update_names(shortName, longName)
    return material

def get_multi_temperature_triga_graphite_material_T0():
    return get_multi_temperature_triga_graphite_material_Ti(0)

def get_multi_temperature_triga_graphite_material_T1():
    return get_multi_temperature_triga_graphite_material_Ti(1)

def get_multi_temperature_triga_graphite_material_T2():
    return get_multi_temperature_triga_graphite_material_Ti(2)

def get_multi_temperature_triga_graphite_material_T3():
    return get_multi_temperature_triga_graphite_material_Ti(3)

def get_multi_temperature_triga_graphite_material_T4():
    return get_multi_temperature_triga_graphite_material_Ti(4)

def get_multi_temperature_triga_graphite_material_T5():
    return get_multi_temperature_triga_graphite_material_Ti(5)

def get_multi_temperature_triga_graphite_material_T6():
    return get_multi_temperature_triga_graphite_material_Ti(6)

def get_multi_temperature_triga_graphite_material_T7():
    return get_multi_temperature_triga_graphite_material_Ti(7)

def get_multi_temperature_triga_graphite_material_T8():
    return get_multi_temperature_triga_graphite_material_Ti(8)

def get_multi_temperature_triga_graphite_material_T9():
    return get_multi_temperature_triga_graphite_material_Ti(9)
    
###############################################################################
def get_multi_temperature_depleted_triga_fuel_material_base():
    return get_depleted_triga_fuel_material()

def get_multi_temperature_triga_fuel_material_Tgrid():
    return [296, 400, 500, 600, 700, 800, 1000, 1200] #K

def get_multi_temperature_depleted_triga_fuel_material_Ti(iT):
    material = get_multi_temperature_depleted_triga_fuel_material_base()
    Tgrid = get_multi_temperature_triga_fuel_material_Tgrid()
    T = Tgrid[iT]
    shortName = 'mtDTFUEL_{}'.format(iT)
    longName = '{} ({} K)'.format(material.longName, T)
    material.update_temperature(T)
    material.update_temperature_index(iT) # X in .9Xc
    # MASS DENSITY SHOULD BE UPDATED TO ACCOUNT FOR THERMAL EXPANSION
    #material.update_mass_density(rho)
    material.update_names(shortName, longName)
    return material

def get_multi_temperature_depleted_triga_fuel_material_T0():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(0)

def get_multi_temperature_depleted_triga_fuel_material_T1():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(1)

def get_multi_temperature_depleted_triga_fuel_material_T2():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(2)

def get_multi_temperature_depleted_triga_fuel_material_T3():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(3)

def get_multi_temperature_depleted_triga_fuel_material_T4():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(4)

def get_multi_temperature_depleted_triga_fuel_material_T5():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(5)

def get_multi_temperature_depleted_triga_fuel_material_T6():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(6)

def get_multi_temperature_depleted_triga_fuel_material_T7():
    return get_multi_temperature_depleted_triga_fuel_material_Ti(7)

###############################################################################

def get_multi_temperature_triga_b4c_material_base():
    return get_triga_b4c_material()

def get_multi_temperature_triga_b4c_material_Tgrid():
    return [296, 400, 500, 600, 700, 800, 1000, 1200] #K

def get_multi_temperature_triga_b4c_material_Ti(iT):
    material = get_multi_temperature_triga_b4c_material_base()
    Tgrid = get_multi_temperature_triga_b4c_material_Tgrid()
    T = Tgrid[iT]
    shortName = 'mtTB4C_{}'.format(iT)
    longName = '{} ({} K)'.format(material.longName, T)
    material.update_temperature(T)
    material.update_temperature_index(iT) # X in .9Xc
    # MASS DENSITY SHOULD BE UPDATED TO ACCOUNT FOR THERMAL EXPANSION
    #material.update_mass_density(rho)
    material.update_names(shortName, longName)
    return material

def get_multi_temperature_triga_b4c_material_T0():
    return get_multi_temperature_triga_b4c_material_Ti(0)

def get_multi_temperature_triga_b4c_material_T5():
    return get_multi_temperature_triga_b4c_material_Ti(5)

def get_multi_temperature_triga_b4c_material_T7():
    return get_multi_temperature_triga_b4c_material_Ti(7)


###############################################################################

def get_all_isotopes(elemDict):
    symList = elemDict.keys()
    symDict = {}
    ZList = []
    ZAList = []
    for sym in symList:
        Z = nd.sym2z[sym.capitalize()]
        ZList.append(Z)
        symDict[Z] = sym
        if sym == 'Th':
            ZAList += get_Th_isotopes()
        elif sym == 'Pa':
            ZAList += get_Pa_isotopes()
        elif sym == 'U':
            ZAList += get_U_isotopes()
        elif sym == 'Np':
            ZAList += get_Np_isotopes()
        elif sym == 'Pu':
            ZAList += get_Pu_isotopes()
        elif sym == 'Am':
            ZAList += get_Am_isotopes()
        elif sym == 'Cm':
            ZAList += get_Cm_isotopes()
        elif sym == 'Bk':
            ZAList += get_Bk_isotopes()
        elif sym == 'Cf':
            ZAList += get_Cf_isotopes()
        elif sym == 'Es':
            ZAList += get_Es_isotopes()
        elif sym == 'Fm':
            ZAList += get_Fm_isotopes() 
        else:
            ZAList += get_isotope_ZAs(Z)
    return symDict, ZList, ZAList

def get_isotope_ZAs(Z, cutoff=0.005):
    '''Get all isotopes with natural abundance at least cutoff for element Z.
    nd.isotopes does not return any metastable A's.'''
    ''' Skip isotopes with only metastable isomers'''
    AList = [A for A in nd.isotopes[Z] if 0.0 in nd.nuclides[(Z,A)] \
             if nd.nuc(Z, A)['abundance'].nominal_value > cutoff]
    return [(Z, A) for A in AList]

def get_Th_isotopes():
    ZAList = []
    ZAList.append((90, 227))
    ZAList.append((90, 228))
    ZAList.append((90, 229))
    ZAList.append((90, 230))
    ZAList.append((90, 231))
    ZAList.append((90, 232))
    ZAList.append((90, 233))
    ZAList.append((90, 234))
    return ZAList

def get_Pa_isotopes():
    ZAList = []
    ZAList.append((91, 229))
    ZAList.append((91, 230))
    ZAList.append((91, 231))
    ZAList.append((91, 232))
    ZAList.append((91, 233))
    return ZAList

def get_U_isotopes():
    ZAList = []
    ZAList.append((92, 230))
    ZAList.append((92, 231))
    ZAList.append((92, 232))
    ZAList.append((92, 233))
    ZAList.append((92, 234))
    ZAList.append((92, 235))
    ZAList.append((92, 236))
    ZAList.append((92, 237))
    ZAList.append((92, 238))
    ZAList.append((92, 239))
    ZAList.append((92, 240))
    ZAList.append((92, 241))
    return ZAList

def get_Np_isotopes():
    ZAList = []
    ZAList.append((93, 234))
    ZAList.append((93, 235))
    ZAList.append((93, 236))
    ZAList.append((93, 237))
    ZAList.append((93, 238))
    ZAList.append((93, 239))
    return ZAList

def get_Pu_isotopes():
    ZAList = []
    ZAList.append((94, 236))
    ZAList.append((94, 237))
    ZAList.append((94, 238))
    ZAList.append((94, 239))
    ZAList.append((94, 240))
    ZAList.append((94, 241))
    ZAList.append((94, 242))
    ZAList.append((94, 243))
    ZAList.append((94, 244))
    ZAList.append((94, 246))
    return ZAList

def get_Am_isotopes():
    ZAList = []
    ZAList.append((95, 240))
    ZAList.append((95, 241))
    ZAList.append((95, 242))
    ZAList.append((95, 642)) # metastable
    ZAList.append((95, 243))
    ZAList.append((95, 244))
    ZAList.append((95, 644)) # metastable
    return ZAList

def get_Cm_isotopes():
    ZAList = []
    ZAList.append((96, 240))
    ZAList.append((96, 241))
    ZAList.append((96, 242))
    ZAList.append((96, 243))
    ZAList.append((96, 244))
    ZAList.append((96, 245))
    ZAList.append((96, 246))
    ZAList.append((96, 247))
    ZAList.append((96, 248))
    ZAList.append((96, 249))
    ZAList.append((96, 250))
    return ZAList

def get_Bk_isotopes():
    ZAList = []
    ZAList.append((97, 245))
    ZAList.append((97, 246))
    ZAList.append((97, 247))
    ZAList.append((97, 248))
    ZAList.append((97, 249))
    ZAList.append((97, 250))
    return ZAList

def get_Cf_isotopes():
    ZAList = []
    ZAList.append((98, 246))
    ZAList.append((98, 248))
    ZAList.append((98, 249))
    ZAList.append((98, 250))
    ZAList.append((98, 251))
    ZAList.append((98, 252))
    ZAList.append((98, 253))
    ZAList.append((98, 254))
    return ZAList

def get_Es_isotopes():
    ZAList = []
    ZAList.append((99, 251))
    ZAList.append((99, 252))
    ZAList.append((99, 253))
    ZAList.append((99, 254))
    ZAList.append((99, 654)) # metastable
    ZAList.append((99, 255))
    return ZAList

def get_Fm_isotopes():
    ZAList = []
    ZAList.append((100, 255))
    return ZAList
    

###############################################################################
def lookup_natl_abundances(ZAList):
    '''Following MCNP, metastable states have A increased by 400: e.g., Am-242m has an A of 642'''
    Zset = set([Z for (Z,A) in ZAList])
    abundanceDict = {}
    for Zelem in Zset:
        AList = [A for (Z,A) in ZAList if Z == Zelem]
        # Use ground-state abundances as default metastable abundances (may override later)
        abundanceList = [nd.nuc(Zelem,A%400)['abundance'].nominal_value for A in AList]
        maxIndex = np.argmax(abundanceList)
        norm = np.sum(abundanceList)
        if norm:
            abundanceList[maxIndex] *= (1.0 / norm)
        for A, abundance in zip(AList, abundanceList):
            abundanceDict[(Zelem,A)] = abundance
    return abundanceDict

def override_abundances_as_elemental(ZAList, abundanceDict, sym):
    '''Override isotopes and abundances for element sym to be elemental values (used for carbon)'''
    Zthis = nd.sym2z[sym]
    AList = [A for (Z,A) in ZAList if Z == Zthis]
    for A in AList:
        i = ZAList.index((Zthis, A))
        del(ZAList[i])
        del(abundanceDict[(Zthis, A)])
    ZAList.append((Zthis,0))
    abundanceDict[(Zthis, 0)] = 1.0

def override_abundances(ZAList, abundanceDict, FractionsDict, sym, AoM = 'Atom'):
    '''Override isotopes and abundances for element given by sym'''
    '''set AoM = 'Atom' if atomFrac is used, otherwise use 'Mass' '''
    Zthis = nd.sym2z[sym]
    AList = [A for (Z,A) in ZAList if Z == Zthis]
    #
    # Zero-out existing abundances
    for A in AList:
        abundanceDict[(Zthis, A)] = 0.0
    #
    # Replace with abundances in atomFractionsDict
    if not FractionsDict:
        raise ValueError('FractionsDict for {0} must be non-empty.'.format(sym))
    # Python guarantees values() and keys() are congruent if no changes to the dict are made between calls
    atomFractionsList = np.array(FractionsDict.values())
    atomFractionsKeys = FractionsDict.keys()
    if AoM != 'Atom':  # If mass fraction are given, convert to atom fraction
        atomMolarMassList = [nd.nuc(Zthis, A%400)['weight'].nominal_value for A in atomFractionsKeys]
        atomFractionsList = [ massFrac/molarMass for massFrac, molarMass in zip(\
                             atomMolarMassList, atomFractionsList)]
    norm = np.sum(atomFractionsList)
    if norm == 0.:
        # If all atom fractions are zero, normalize by making each equal to 1/(# isotopes)
        numIsotopes = len(atomFractionsList)
        for A in AList:
            abundanceDict[(Zthis, A)] = 1. / numIsotopes
    elif norm > 1.1 or norm < 0.9:
        # If atom fractions are very unnormalized, multiplicatively normalize
        for A in atomFractionsKeys:
            abundanceDict[(Zthis, A)] = FractionsDict[A] / norm
    else:
        # Else, normalize by changing the abundance of the most abundant isotope
        majorA = atomFractionsKeys[np.argmax(atomFractionsList)]
        partialSum = np.sum([FractionsDict[A] for A in atomFractionsKeys if A != majorA])
        FractionsDict[majorA] = 1.0 - partialSum
        for A in atomFractionsKeys:
            abundanceDict[(Zthis, A)] = FractionsDict[A]
    #
    # Add in new isotopes to ZAList
    newAs = [A for A in atomFractionsKeys if (Zthis, A) not in ZAList]
    for A in newAs:
        ZAList.append((Zthis, A))
    #
    # Remove entries with zero abundances
    for A in AList:
        if abundanceDict[(Zthis, A)] == 0.0:
            i = ZAList.index((Zthis, A))
            del(ZAList[i])
            del(abundanceDict[(Zthis, A)])

###############################################################################
def print_materials(materials, verbosity=False):
    if verbosity:
        for i, material in enumerate(materials):
            print '------- Material {0} -------'.format(i)
            material.print_contents(verbosity)

###############################################################################
class Material():
    def __init__(self, shortName=None, longName=None, temperature=None, atomDensity=None, massDensity=None, chordLength=None, abundanceDict=None, elemAtomFracDict=None, elemMassFracDict=None, ZAList=None, ZList=None, symDict=None, backgroundXSDict=None, thermalOpt=0, elemWeightDict=None, matlWeight=None, SabDict=None, thermalXSDict=None, temperatureIndex=0):
        '''The following units are used:
        temperature in Kelvin is the temperature of the material
        temperatureIndex is the least-significant digit of an MCNP-like matl. name and refers to temperature
        atomDensity in atoms/barn-cm is the atom density of the material
        massDensity in g/cm^3 is the mass density of the material
        chordLength in cm is used to calculate the escape cross section; set to zero to use 0 escape XS
        abundanceDict is the atom fraction of each isotope in its element
        elemAtomFracDict is the atom fraction of each element in the material
        elemMassFracDict is the mass/weight fraction of each element in the material
        elemWeightDict is the elemental mass/weight in g/mole calculated using the correct abundances
        matlWeight in g/mole is the effective weight of the material
        ZAList is a list of all (Z,A) = (atomic number, atomic mass) pairs in the material
        ZList is a list of all elements in the material stored as atomic number
        symDict is the chemical symbol for each element in the material
        backgroundXSDict is an approximate background XS seen by each nuclide in the material
        thermalOpt specifies which thermal treatment to use
        SabDict is the thermal S(alpha,beta) Hollerith string used for each nuclide in the material
        thermalXSDict is a list of thermal XS used for each nuclide (list of shortName's in endfMTList)
        shortName is a succinct name without whitespaces
        longName is a longer name that may contain whitespace
        '''
        # locals() includes local names, including 'self'. Update Material to include all keywords above.
        varss = locals()
        self.__dict__.update(varss)
        del self.__dict__["self"]
        self.setup()

    def setup(self):
        '''Initialize attributes. Prefer atom fractions and mass densities over mass fractions and atom densities if both are given.'''
        self.make_lists_sets()
        self.strip_short_name()
        #
        self.calc_and_store_elem_weight()
        #
        if self.elemAtomFracDict:
            self.change_atom_frac_dict_keys_to_Z()
            self.calc_and_store_elem_mass_frac()
        elif self.elemMassFracDict:
            self.change_mass_frac_dict_keys_to_Z()
            self.calc_and_store_elem_atom_frac()
        else:
            raise ValueError('Must set either elemAtomFracDict or elemMassFracDict')
        #
        self.calc_and_store_matl_weight()
        #
        if self.massDensity:
            self.calc_and_store_atom_density()
        elif self.atomDensity:
            self.calc_and_store_mass_density()
        else:
            raise ValueError('Must set either atomDensity or massDensity')
        #
        self.set_sab_dict()
        self.set_thermal_xs_dict()
        self.check_internal_keys_consistency()

    def copy(self):
        return copy.deepcopy(self)

    def update_names(self, shortName, longName):
        self.shortName = shortName
        self.longName = longName

    def update_thermal_option(self, thermalOpt):
        self.thermalOpt = thermalOpt
        self.set_sab_dict()
        self.set_thermal_xs_dict()

    def update_temperature(self, temperature):
        self.temperature = temperature

    def update_temperature_index(self, temperatureIndex):
        self.temperatureIndex = temperatureIndex

    def update_chord_length(self, chordLength):
        self.chordLength = chordLength

    def update_mass_density(self, massDensity):
        self.massDensity = massDensity
        self.calc_and_store_atom_density()

    def update_atom_density(self, atomDensity):
        self.atomDensity = atomDensity
        self.calc_and_store_mass_density()

    def update_atom_fractions_and_atom_density(self, elemAtomFracDict, atomDensity):
        self.elemAtomFracDict = elemAtomFracDict
        self.calc_and_store_elem_mass_frac()
        self.calc_and_store_matl_weight()
        self.update_atom_density(atomDensity)

    def update_atom_fractions_and_mass_density(self, elemAtomFracDict, massDensity):
        self.elemAtomFracDict = elemAtomFracDict
        self.calc_and_store_elem_mass_frac()
        self.calc_and_store_matl_weight()
        self.update_mass_density(massDensity)

    def update_mass_fractions_and_atom_density(self, elemMassFracDict, atomDensity):
        self.elemMassFracDict = elemMassFracDict
        self.calc_and_store_elem_atom_frac()
        self.calc_and_store_matl_weight()
        self.update_atom_density(atomDensity)

    def update_mass_fractions_and_mass_density(self, elemMassFracDict, massDensity):
        self.elemMassFracDict = elemMassFracDict
        self.calc_and_store_elem_atom_frac()
        self.calc_and_store_matl_weight()
        self.update_mass_density(massDensity)

    ################################################################
    def print_contents(self, verbosity=0):
        if verbosity:
            strs = ['shortName', 'longName']
            for strr in strs:
                print strr, getattr(self, strr)
            #
            strr = 'thermalOpt'
            val = getattr(self, strr)
            print strr, val
            #
            strs = [('chordLength', 'cm'), ('temperature', 'K'), ('atomDensity', '1/b-cm'), ('massDensity', 'g/cc') ]
            for (strr, unit) in strs:
                print strr, getattr(self, strr), '({0})'.format(unit)
            #
        if verbosity > 1:
            strr, unit =  ('matlWeight', 'g/mole')
            print strr, getattr(self, strr), '({0})'.format(unit)
            #
        if verbosity:
            sortedSymList = [self.symDict[Z] for Z in sorted(self.ZList)]
            print 'symList', sortedSymList
            #
        if verbosity > 1:
            strs = ['ZList', 'ZAList']
            for strr in strs:
                print strr, sorted(getattr(self, strr))
            #
            strs = [('abundanceDict', 'atom fraction'), ('elemWeightDict', 'g/mole')]
            for (strr, unit) in strs:
                print strr, sorted(getattr(self, strr).items()), '({0})'.format(unit)
            #
            strs = ['elemAtomFracDict', 'elemMassFracDict']
            for strr in strs:
                print strr, sorted(getattr(self, strr).items())
            #
            strs = ['SabDict', 'thermalXSDict', 'backgroundXSDict']
            for strr in strs:
                print strr, sorted(getattr(self, strr).items())
            #

    ################################################################
    def make_lists_sets(self):
        self.ZAList = set(self.ZAList)
        self.ZList = set(self.ZList)

    def check_internal_keys_consistency(self):
        if self.shortName.count(' '):
            raise ValueError('shortName should not contain spaces')
        if set(self.abundanceDict.keys()) != self.ZAList:
            raise ValueError('ZAList should be the keys for abundanceDict')
        if set(self.elemAtomFracDict.keys()) != self.ZList:
            raise ValueError('ZList should be the keys for elemAtomFracDict')
        if set(self.elemMassFracDict.keys()) != self.ZList:
            raise ValueError('ZList should be the keys for elemMassFracDict')
        if set(self.elemWeightDict.keys()) != self.ZList:
            raise ValueError('ZList should be the keys for elemWeightDict')
        if set(self.SabDict.keys()) != self.ZAList:
            raise ValueError('ZAList should be the keys for SabDict')
        if set(self.thermalXSDict.keys()) != self.ZAList:
            raise ValueError('ZAList should be the keys for thermalXSDict')
        if set(self.symDict.keys()) != self.ZList:
            raise ValueError('ZList should be the keys for consistent with symDict')
        if set([Z for (Z, A) in self.ZAList]) != self.ZList:
            raise ValueError('ZList should be consistent with ZAList')

    def strip_short_name(self):
        '''Remove whitespace from shortName'''
        namePieces = self.shortName.split()
        namePieces = [piece.strip() for piece in namePieces]
        self.shortName = ''.join(namePieces)

    def change_atom_frac_dict_keys_to_Z(self):
        '''Change keys from using sym to using Z'''
        atomFracDictFromSym = self.elemAtomFracDict
        atomFracDictFromZ = {}
        for sym in atomFracDictFromSym.keys():
            atomFracDictFromZ[nd.sym2z[sym]] = atomFracDictFromSym[sym]
        self.elemAtomFracDict = atomFracDictFromZ

    def change_mass_frac_dict_keys_to_Z(self):
        '''Change keys from using sym to using Z'''
        massFracDictFromSym = self.elemMassFracDict
        massFracDictFromZ = {}
        for sym in massFracDictFromSym.keys():
            massFracDictFromZ[nd.sym2z[sym]] = massFracDictFromSym[sym]
        self.elemMassFracDict = massFracDictFromZ

    def calc_and_store_elem_weight(self):
        '''Calculate the molar mass of each element from its isotopic abundance.'''
        self.elemWeightDict = {}
        for Zelem in self.ZList:
            AList = [A for (Z,A) in self.ZAList if Z == Zelem]
            elemAtomFracList = [self.abundanceDict[(Zelem,A)] for A in AList]
            if A:
                # For metastable states (A increased by 400), use groundstate weights
                weightList = [nd.nuc(Zelem, A%400)['weight'].nominal_value for A in AList]
                self.elemWeightDict[Zelem] = np.sum(np.multiply(elemAtomFracList, weightList))
            else:
                # A of 0 indicates natural composition (used for carbon)
                self.elemWeightDict[Zelem] = nd.weight(Zelem)

    def normalize_elem_atom_frac(self):
        '''Make sum(elemAtomFracDcit) == 1'''
        norm = np.sum((float(value) for value in self.elemAtomFracDict.values()))
        for key in self.elemAtomFracDict:
            self.elemAtomFracDict[key] /= norm

    def normalize_elem_mass_frac(self):
        '''Make sum(elemMassFracDcit) == 1'''
        norm = np.sum((float(value) for value in self.elemMassFracDict.values()))
        for key in self.elemMassFracDict:
            self.elemMassFracDict[key] /= norm

    def calc_and_store_elem_atom_frac(self):
        '''Convert from weight fractions to atom fractions.'''
        self.normalize_elem_mass_frac()
        self.elemAtomFracDict = {}
        norm = np.sum((self.elemMassFracDict[Z] / self.elemWeightDict[Z] for Z in self.ZList))
        for Z in self.ZList:
            self.elemAtomFracDict[Z] = self.elemMassFracDict[Z] / (self.elemWeightDict[Z] * norm)
        self.normalize_elem_atom_frac()

    def calc_and_store_elem_mass_frac(self):
        '''Convert from atom fractions to weight fractions.'''
        self.normalize_elem_atom_frac()
        self.elemMassFracDict = {}
        norm = np.sum((self.elemAtomFracDict[Z] * self.elemWeightDict[Z] for Z in self.ZList))
        for Z in self.ZList:
            self.elemMassFracDict[Z] = self.elemAtomFracDict[Z] * self.elemWeightDict[Z] / norm
        self.normalize_elem_mass_frac()

    def calc_and_store_matl_weight(self):
        '''Calculate the molar mass of the material. Requires elemWeightDict and elemAtomFracDict be set.'''
        self.matlWeight = np.sum((self.elemWeightDict[Z] * self.elemAtomFracDict[Z] for Z in self.ZList))

    def calc_and_store_atom_density(self):
        '''Convert from g/cm^3 to 1/b-cm. Requires massDensity and matlWeight be set.'''
        self.atomDensity = self.massDensity * util.avogadros_number() / self.matlWeight

    def calc_and_store_mass_density(self):
        '''Convert from 1/b-cm to g/cm^3. Requires atomDensity and matlWeight be set.'''
        self.massDensity = self.matlWeight * self.atomDensity / util.avogadros_number()

    def set_sab_dict(self):
        '''Determine what thermal treatment to use for each nuclide in the material.
        The key is (Z,A) and the value is the element thermal name'''
        thermalName2ZAs = util.get_thermal_name_to_nuclide_list_dict()
        ZthermalName2Sab = util.get_thermal_name_to_element_thermal_name_dict()
        nonBoundSabs = util.get_non_bound_names()
        self.thermalOpt = self.thermalOpt.lower().strip()
        thermalOpt = self.thermalOpt
        self.SabDict = {}
        if thermalOpt == 'free':
            for (Z,A) in self.ZAList:
                # Use a free thermal treatment for all nuclides
                self.SabDict[(Z,A)] = 'free'
        elif thermalOpt in nonBoundSabs:
            for (Z,A) in self.ZAList:
                # Do not use a thermal treatment for any nuclide
                self.SabDict[(Z,A)] = 'none'
        else:
            boundZAList = thermalName2ZAs[thermalOpt]
            for (Z,A) in self.ZAList:
                if (Z,A) in boundZAList:
                    # If S(alpha,beta) applies to current nuclide, use it
                    self.SabDict[(Z,A)] = ZthermalName2Sab[(Z,thermalOpt)]
                else:
                    # Otherwise, use a free thermal treatment
                    self.SabDict[(Z,A)] = 'free'

    def set_thermal_xs_dict(self):
        '''Determine which thermal cross sections are used by each nuclide in the material.
        The key is (Z,A) and the value is a list of thermal xs names'''
        elem2xs = util.get_element_thermal_name_to_thermal_xs_list_dict()
        self.thermalXSDict = {(Z,A): elem2xs[elem] for (Z,A), elem in self.SabDict.items()}

    def check_background_xs_keys_consistency(self):
        if set(self.backgroundXSDict.keys()) != self.ZAList:
            raise ValueError('ZAList should be the keys for backgroundXSDict')
