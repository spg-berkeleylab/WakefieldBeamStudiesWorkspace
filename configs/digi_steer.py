import os
from Gaudi.Configuration import *

from Configurables import LcioEvent, EventDataSvc, MarlinProcessorWrapper
from k4FWCore.parseArgs import parser

parser.add_argument(
    "--DD4hepXMLFile",
    help="Compact detector description file",
    type=str,
    default=os.environ.get("WCD_GEO", ""),
)

parser.add_argument(
    "--OverlayFullPathToMuPlus",
    help="Path to files for muplus BIB overlay",
    type=str,
    default="/path/to/muplus/",
)

parser.add_argument(
    "--OverlayFullPathToMuMinus",
    help="Path to files for muminus BIB overlay",
    type=str,
    default="/path/to/muminus/",
)

parser.add_argument(
    "--OverlayFullNumberBackground",
    help="Number of background files used for BIB overlay",
    type=str,
    default="192", #Magic number assumes 45 phi clones of each MC particle
)

parser.add_argument(
    "--OverlayIPBackgroundFileNames",
    help="Path to files used for incoherent pairs overlay",
    type=str,
    default="/path/to/pairs.slcio",
)

parser.add_argument(
    "--OverlayIPNumberBackground",
    help="Number of background files used for IP overlay",
    type=str,
    default="1", #Magic number associated to the specific simulation setup
)

parser.add_argument(
    "--doOverlayFull",
    help="Do BIB overlay",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doOverlayIP",
    help="Do incoherent pairs overlay",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doFilterDL",
    help="Do double-layer filtering",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doTrkDigiSimple",
    help="Only use simplified tracker digitization",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--doClusterFilter",
    help="Do cluster shape filtering",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--writeAll",
    help="Store all output collections",
    action="store_true",
    default=False,
)


the_args = parser.parse_known_args()[0]

algList = []
evtsvc = EventDataSvc()

read = LcioEvent()
read.OutputLevel = INFO
read.Files = ["input.slcio"]
algList.append(read)

DD4hep = MarlinProcessorWrapper("DD4hep")
DD4hep.OutputLevel = INFO
DD4hep.ProcessorType = "InitializeDD4hep"
DD4hep.Parameters = {
                     "DD4hepXMLFile": [the_args.DD4hepXMLFile],
                     "EncodingStringParameterName": ["GlobalTrackerReadoutID"]
                     }

AIDA = MarlinProcessorWrapper("AIDA")
AIDA.OutputLevel = INFO
AIDA.ProcessorType = "AIDAProcessor"
AIDA.Parameters = {
                   "Compress": ["1"],
                   "FileName": ["output_digi"],
                   "FileType": ["root"]
                   }

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = INFO
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
                          "HowOften": ["1"]
                          }

LCIOWriter_all = MarlinProcessorWrapper("LCIOWriter_all")
LCIOWriter_all.OutputLevel = INFO
LCIOWriter_all.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_all.Parameters = {
                             "DropCollectionNames": [],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": [],
                             "KeepCollectionNames": [],
                             "LCIOOutputFile": ["output_digi.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }

LCIOWriter_light = MarlinProcessorWrapper("LCIOWriter_light")
LCIOWriter_light.OutputLevel = INFO
LCIOWriter_light.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_light.Parameters = {
                               "DropCollectionNames": ["VXDBarrelHits_realDigi", "VXDEndcapHits_realDigi"],# "ITBarrelHits_realDigi", "ITEndcapHits_realDigi", "OTBarrelHits_realDigi", "OTEndcapHits_realDigi"],
                               "DropCollectionTypes": ["SimTrackerHit", "SimCalorimeterHit"],
                               "FullSubsetCollections": [],
                               "KeepCollectionNames": [],
                               "LCIOOutputFile": ["output_digi_light.slcio"],
                               "LCIOWriteMode": ["WRITE_NEW"]
                               }

VXDBarrelDigitiser = MarlinProcessorWrapper("VXDBarrelDigitiser")
VXDBarrelDigitiser.OutputLevel = INFO
VXDBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDBarrelDigitiser.Parameters = {
                                 "CorrectTimesForPropagation": ["true"],
                                 "IsStrip": ["false"],
                                 "ResolutionT": ["0.03"],
                                 "ResolutionU": ["0.005"],
                                 "ResolutionV": ["0.005"],
                                 "SimTrackHitCollectionName": ["VertexBarrelCollection"],
                                 "SimTrkHitRelCollection": ["VXDBarrelHitsRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TimeWindowMax": ["0.15"],
                                 "TimeWindowMin": ["-0.09"],
                                 "TrackerHitCollectionName": ["VXDBarrelHits"],
                                 "UseTimeWindow": ["true"]
                                 }

VXDEndcapDigitiser = MarlinProcessorWrapper("VXDEndcapDigitiser")
VXDEndcapDigitiser.OutputLevel = INFO
VXDEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDEndcapDigitiser.Parameters = {
                                 "CorrectTimesForPropagation": ["true"],
                                 "IsStrip": ["false"],
                                 "ResolutionT": ["0.03"],
                                 "ResolutionU": ["0.005"],
                                 "ResolutionV": ["0.005"],
                                 "SimTrackHitCollectionName": ["VertexEndcapCollection"],
                                 "SimTrkHitRelCollection": ["VXDEndcapHitsRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TimeWindowMax": ["0.15"],
                                 "TimeWindowMin": ["-0.09"],
                                 "TrackerHitCollectionName": ["VXDEndcapHits"],
                                 "UseTimeWindow": ["true"]
                                 }

ITBarrelDigitiser = MarlinProcessorWrapper("ITBarrelDigitiser")
ITBarrelDigitiser.OutputLevel = INFO
ITBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
ITBarrelDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["InnerTrackerBarrelCollection"],
                                "SimTrkHitRelCollection": ["ITBarrelHitsRelations"],
                                "SubDetectorName": ["InnerTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["ITBarrelHits"],
                                "UseTimeWindow": ["true"]
                                }

ITEndcapDigitiser = MarlinProcessorWrapper("ITEndcapDigitiser")
ITEndcapDigitiser.OutputLevel = INFO
ITEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
ITEndcapDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["InnerTrackerEndcapCollection"],
                                "SimTrkHitRelCollection": ["ITEndcapHitsRelations"],
                                "SubDetectorName": ["InnerTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["ITEndcapHits"],
                                "UseTimeWindow": ["true"]
                                }

OTBarrelDigitiser = MarlinProcessorWrapper("OTBarrelDigitiser")
OTBarrelDigitiser.OutputLevel = INFO
OTBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
OTBarrelDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["OuterTrackerBarrelCollection"],
                                "SimTrkHitRelCollection": ["OTBarrelHitsRelations"],
                                "SubDetectorName": ["OuterTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["OTBarrelHits"],
                                "UseTimeWindow": ["true"]
                                }

OTEndcapDigitiser = MarlinProcessorWrapper("OTEndcapDigitiser")
OTEndcapDigitiser.OutputLevel = INFO
OTEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
OTEndcapDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["OuterTrackerEndcapCollection"],
                                "SimTrkHitRelCollection": ["OTEndcapHitsRelations"],
                                "SubDetectorName": ["OuterTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["OTEndcapHits"],
                                "UseTimeWindow": ["true"]
                                }


VXDBarrelRealisticDigi = MarlinProcessorWrapper("VXDBarrelRealisticDigi")
VXDBarrelRealisticDigi.OutputLevel = INFO
VXDBarrelRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
VXDBarrelRealisticDigi.Parameters = {
                                     "ChargeDigitizeBinning": ["1"],
                                     "ChargeDigitizeNumBits": ["4"],
                                     "ChargeMaximum": ["15000."],
                                     "CollectionName": ["VertexBarrelCollection"],
                                     "CutOnDeltaRays": ["0.030"],
                                     "Diffusion": ["0.07"],
                                     "DigitizeCharge": ["1"],
                                     "DigitizeTime": ["0"],
                                     "ElectronicEffects": ["1"],
                                     "ElectronicNoise": ["80"],
                                     "ElectronsPerKeV": ["270.3"],
                                     "EnergyLoss": ["280.0"],
                                     "MaxEnergyDelta": ["100.0"],
                                     "MaxTrackLength": ["10.0"],
                                     "OutputCollectionName": ["VXDBarrelHits_realDigi"],
                                     "PixelSizeX": ["0.025"],
                                     "PixelSizeY": ["0.025"],
                                     "PoissonSmearing": ["1"],
                                     "RelationColName": ["VXDBarrelHitsRelations_realDigi"],
                                     "SegmentLength": ["0.005"],
                                     "StoreFiredPixels": ["1"],
                                     "SubDetectorName": ["VertexBarrel"],
                                     "TanLorentz": ["0.8"],
                                     "TanLorentzY": ["0.0"],
                                     "Threshold": ["500"],
                                     "ThresholdSmearSigma": ["25"],
                                     "TimeDigitizeBinning": ["0"],
                                     "TimeDigitizeNumBits": ["10"],
                                     "TimeMaximum": ["15.0"],
                                     "TimeSmearingSigma": ["0.03"]
                                     }

VXDEndcapRealisticDigi = MarlinProcessorWrapper("VXDEndcapRealisticDigi")
VXDEndcapRealisticDigi.OutputLevel = INFO
VXDEndcapRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
VXDEndcapRealisticDigi.Parameters = {
                                     "ChargeDigitizeBinning": ["1"],
                                     "ChargeDigitizeNumBits": ["4"],
                                     "ChargeMaximum": ["15000."],
                                     "CollectionName": ["VertexEndcapCollection"],
                                     "CutOnDeltaRays": ["0.030"],
                                     "Diffusion": ["0.07"],
                                     "DigitizeCharge": ["1"],
                                     "DigitizeTime": ["0"],
                                     "ElectronicEffects": ["1"],
                                     "ElectronicNoise": ["80"],
                                     "ElectronsPerKeV": ["270.3"],
                                     "EnergyLoss": ["280.0"],
                                     "MaxEnergyDelta": ["100.0"],
                                     "MaxTrackLength": ["10.0"],
                                     "OutputCollectionName": ["VXDEndcapHits_realDigi"],
                                     "PixelSizeX": ["0.025"],
                                     "PixelSizeY": ["0.025"],
                                     "PoissonSmearing": ["1"],
                                     "RelationColName": ["VXDEndcapHitsRelations_realDigi"],
                                     "SegmentLength": ["0.005"],
                                     "StoreFiredPixels": ["1"],
                                     "SubDetectorName": ["VertexEndcap"],
                                     "TanLorentz": ["0.0"],
                                     "TanLorentzY": ["0.0"],
                                     "Threshold": ["500"],
                                     "ThresholdSmearSigma": ["25"],
                                     "TimeDigitizeBinning": ["0"],
                                     "TimeDigitizeNumBits": ["10"],
                                     "TimeMaximum": ["15.0"],
                                     "TimeSmearingSigma": ["0.03"]
                                     }

InnerPlanarRealisticDigi = MarlinProcessorWrapper("InnerPlanarRealisticDigi")
InnerPlanarRealisticDigi.OutputLevel = INFO
InnerPlanarRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
InnerPlanarRealisticDigi.Parameters = {
                                       "ChargeDigitizeBinning": ["1"],
                                       "ChargeDigitizeNumBits": ["4"],
                                       "ChargeMaximum": ["60000."],
                                       "CollectionName": ["InnerTrackerBarrelCollection"],
                                       "CutOnDeltaRays": ["0.030"],
                                       "Diffusion": ["0.07"],
                                       "DigitizeCharge": ["1"],
                                       "DigitizeTime": ["0"],
                                       "ElectronicEffects": ["1"],
                                       "ElectronicNoise": ["80"],
                                       "ElectronsPerKeV": ["270.3"],
                                       "EnergyLoss": ["280.0"],
                                       "MaxEnergyDelta": ["100.0"],
                                       "MaxTrackLength": ["10.0"],
                                       "OutputCollectionName": ["ITBarrelHits_realDigi"],
                                       "PixelSizeX": ["0.050"],
                                       "PixelSizeY": ["1.0"],
                                       "PoissonSmearing": ["1"],
                                       "RelationColName": ["ITBarrelHitsRelations_realDigi"],
                                       "SegmentLength": ["0.005"],
                                       "StoreFiredPixels": ["1"],
                                       "SubDetectorName": ["InnerTrackerBarrel"],
                                       "TanLorentz": ["0.8"],
                                       "TanLorentzY": ["0.0"],
                                       "Threshold": ["1000."],
                                       "ThresholdSmearSigma": ["25"],
                                       "TimeDigitizeBinning": ["0"],
                                       "TimeDigitizeNumBits": ["10"],
                                       "TimeMaximum": ["15.0"],
                                       "TimeSmearingSigma": ["0.060"]
                                       }

InnerEndcapRealisticDigi = MarlinProcessorWrapper("InnerEndcapRealisticDigi")
InnerEndcapRealisticDigi.OutputLevel = INFO
InnerEndcapRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
InnerEndcapRealisticDigi.Parameters = {
                                       "ChargeDigitizeBinning": ["1"],
                                       "ChargeDigitizeNumBits": ["4"],
                                       "ChargeMaximum": ["60000."],
                                       "CollectionName": ["InnerTrackerEndcapCollection"],
                                       "CutOnDeltaRays": ["0.030"],
                                       "Diffusion": ["0.07"],
                                       "DigitizeCharge": ["1"],
                                       "DigitizeTime": ["0"],
                                       "ElectronicEffects": ["1"],
                                       "ElectronicNoise": ["80"],
                                       "ElectronsPerKeV": ["270.3"],
                                       "EnergyLoss": ["280.0"],
                                       "MaxEnergyDelta": ["100.0"],
                                       "MaxTrackLength": ["10.0"],
                                       "OutputCollectionName": ["ITEndcapHits_realDigi"],
                                       "PixelSizeX": ["0.050"],
                                       "PixelSizeY": ["1.0"],
                                       "PoissonSmearing": ["1"],
                                       "RelationColName": ["ITEndcapHitsRelations_realDigi"],
                                       "SegmentLength": ["0.005"],
                                       "StoreFiredPixels": ["1"],
                                       "SubDetectorName": ["InnerTrackerEndcap"],
                                       "TanLorentz": ["0.0"],
                                       "TanLorentzY": ["0.0"],
                                       "Threshold": ["1000."],
                                       "ThresholdSmearSigma": ["25"],
                                       "TimeDigitizeBinning": ["0"],
                                       "TimeDigitizeNumBits": ["10"],
                                       "TimeMaximum": ["15.0"],
                                       "TimeSmearingSigma": ["0.060"]
                                       }

OuterPlanarRealisticDigi = MarlinProcessorWrapper("OuterPlanarRealisticDigi")
OuterPlanarRealisticDigi.OutputLevel = INFO
OuterPlanarRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
OuterPlanarRealisticDigi.Parameters = {
                                       "ChargeDigitizeBinning": ["1"],
                                       "ChargeDigitizeNumBits": ["4"],
                                       "ChargeMaximum": ["60000."],
                                       "CollectionName": ["OuterTrackerBarrelCollection"],
                                       "CutOnDeltaRays": ["0.030"],
                                       "Diffusion": ["0.07"],
                                       "DigitizeCharge": ["1"],
                                       "DigitizeTime": ["0"],
                                       "ElectronicEffects": ["1"],
                                       "ElectronicNoise": ["80"],
                                       "ElectronsPerKeV": ["270.3"],
                                       "EnergyLoss": ["280.0"],
                                       "MaxEnergyDelta": ["100.0"],
                                       "MaxTrackLength": ["10.0"],
                                       "OutputCollectionName": ["OTBarrelHits_realDigi"],
                                       "PixelSizeX": ["0.050"],
                                       "PixelSizeY": ["10.0"],
                                       "PoissonSmearing": ["1"],
                                       "RelationColName": ["OTBarrelHitsRelations_realDigi"],
                                       "SegmentLength": ["0.005"],
                                       "StoreFiredPixels": ["1"],
                                       "SubDetectorName": ["OuterTrackerBarrel"],
                                       "TanLorentz": ["0.8"],
                                       "TanLorentzY": ["0.0"],
                                       "Threshold": ["1000."],
                                       "ThresholdSmearSigma": ["25"],
                                       "TimeDigitizeBinning": ["0"],
                                       "TimeDigitizeNumBits": ["10"],
                                       "TimeMaximum": ["15.0"],
                                       "TimeSmearingSigma": ["0.060"]
                                       }

OuterEndcapRealisticDigi = MarlinProcessorWrapper("OuterEndcapRealisticDigi")
OuterEndcapRealisticDigi.OutputLevel = INFO
OuterEndcapRealisticDigi.ProcessorType = "MuonCVXDDigitiser"
OuterEndcapRealisticDigi.Parameters = {
                                       "ChargeDigitizeBinning": ["1"],
                                       "ChargeDigitizeNumBits": ["4"],
                                       "ChargeMaximum": ["60000."],
                                       "CollectionName": ["OuterTrackerEndcapCollection"],
                                       "CutOnDeltaRays": ["0.030"],
                                       "Diffusion": ["0.07"],
                                       "DigitizeCharge": ["1"],
                                       "DigitizeTime": ["0"],
                                       "ElectronicEffects": ["1"],
                                       "ElectronicNoise": ["80"],
                                       "ElectronsPerKeV": ["270.3"],
                                       "EnergyLoss": ["280.0"],
                                       "MaxEnergyDelta": ["100.0"],
                                       "MaxTrackLength": ["10.0"],
                                       "OutputCollectionName": ["OTEndcapHits_realDigi"],
                                       "PixelSizeX": ["0.050"],
                                       "PixelSizeY": ["10.0"],
                                       "PoissonSmearing": ["1"],
                                       "RelationColName": ["OTEndcapHitsRelations_realDigi"],
                                       "SegmentLength": ["0.005"],
                                       "StoreFiredPixels": ["1"],
                                       "SubDetectorName": ["OuterTrackerEndcap"],
                                       "TanLorentz": ["0.0"],
                                       "TanLorentzY": ["0.0"],
                                       "Threshold": ["1000."],
                                       "ThresholdSmearSigma": ["25"],
                                       "TimeDigitizeBinning": ["0"],
                                       "TimeDigitizeNumBits": ["10"],
                                       "TimeMaximum": ["15.0"],
                                       "TimeSmearingSigma": ["0.060"]
                                       }


ECalBarrelDigi = MarlinProcessorWrapper("ECalBarrelDigi")
ECalBarrelDigi.OutputLevel = INFO
ECalBarrelDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalBarrelCollection"],
    "outputHitCollections": ["EcalBarrelCollectionDigi"],
    "outputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalBarrelReco = MarlinProcessorWrapper("ECalBarrelReco")
ECalBarrelReco.OutputLevel = INFO
ECalBarrelReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalBarrelCollectionDigi"],
    "inputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["EcalBarrelCollectionRec"],
    "outputRelationCollections": ["EcalBarrelRelationsSimRec"]
}

ECalPlugDigi = MarlinProcessorWrapper("ECalPlugDigi")
ECalPlugDigi.OutputLevel = INFO
ECalPlugDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalPlugDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalPlugCollection"],
    "outputHitCollections": ["ECalPlugCollectionDigi"],
    "outputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalPlugReco = MarlinProcessorWrapper("ECalPlugReco")
ECalPlugReco.OutputLevel = INFO
ECalPlugReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalPlugReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["ECalPlugCollectionDigi"],
    "inputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "outputHitCollections": ["ECalPlugCollectionRec"],
    "outputRelationCollections": ["ECalPlugRelationsSimRec"]
}

ECalEndcapDigi = MarlinProcessorWrapper("ECalEndcapDigi")
ECalEndcapDigi.OutputLevel = INFO
ECalEndcapDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalEndcapCollection"],
    "outputHitCollections": ["EcalEndcapCollectionDigi"],
    "outputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalEndcapReco = MarlinProcessorWrapper("ECalEndcapReco")
ECalEndcapReco.OutputLevel = INFO
ECalEndcapReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalEndcapCollectionDigi"],
    "inputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["EcalEndcapCollectionRec"],
    "outputRelationCollections": ["EcalEndcapRelationsSimRec"]
}

HCalBarrelDigi = MarlinProcessorWrapper("HCalBarrelDigi")
HCalBarrelDigi.OutputLevel = INFO
HCalBarrelDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004925"],
    "inputHitCollections": ["HCalBarrelCollection"],
    "outputHitCollections": ["HcalBarrelCollectionDigi"],
    "outputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalBarrelReco = MarlinProcessorWrapper("HCalBarrelReco")
HCalBarrelReco.OutputLevel = INFO
HCalBarrelReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0287783798145"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalBarrelCollectionDigi"],
    "inputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["HcalBarrelCollectionRec"],
    "outputRelationCollections": ["HcalBarrelRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalEndcapDigi = MarlinProcessorWrapper("HCalEndcapDigi")
HCalEndcapDigi.OutputLevel = INFO
HCalEndcapDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalEndcapCollection"],
    "outputHitCollections": ["HcalEndcapCollectionDigi"],
    "outputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalEndcapReco = MarlinProcessorWrapper("HCalEndcapReco")
HCalEndcapReco.OutputLevel = INFO
HCalEndcapReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalEndcapCollectionDigi"],
    "inputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["HcalEndcapCollectionRec"],
    "outputRelationCollections": ["HcalEndcapRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalRingDigi = MarlinProcessorWrapper("HCalRingDigi")
HCalRingDigi.OutputLevel = INFO
HCalRingDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalRingDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalRingCollection"],
    "outputHitCollections": ["HCalRingCollectionDigi"],
    "outputRelationCollections": ["HCalRingRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalRingReco = MarlinProcessorWrapper("HCalRingReco")
HCalRingReco.OutputLevel = INFO
HCalRingReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalRingReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HCalRingCollectionDigi"],
    "inputRelationCollections": ["HCalRingRelationsSimDigi"],
    "outputHitCollections": ["HCalRingCollectionRec"],
    "outputRelationCollections": ["HCalRingRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MuonDigitiser = MarlinProcessorWrapper("MuonDigitiser")
MuonDigitiser.OutputLevel = INFO
MuonDigitiser.ProcessorType = "DDSimpleMuonDigi"
MuonDigitiser.Parameters = {
                            "CalibrMUON": ["70.1"],
                            "MUONCollections": ["YokeBarrelCollection", "YokeEndcapCollection"],
                            "MUONOutputCollection": ["MuonHits"],
                            "MaxHitEnergyMUON": ["2.0"],
                            "MuonThreshold": ["1e-06"],
                            "RelationOutputCollection": ["MuonHitsRelations"]
                            }

FilterDL_VXDB = MarlinProcessorWrapper("FilterDL_VXDB")
FilterDL_VXDB.OutputLevel = INFO
FilterDL_VXDB.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDB.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.0", "35.0", "2", "3", "1.7", "18.0", "4", "5", "1.5", "10.0", "6", "7", "1.4", "6.5"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDBarrelHits"],
                            "OutputCollection": ["VXDBarrelHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

FilterDL_VXDE = MarlinProcessorWrapper("FilterDL_VXDE")
FilterDL_VXDE.OutputLevel = INFO
FilterDL_VXDE.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDE.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.2", "8.0", "2", "3", "1.4", "2.8", "4", "5", "0.86", "0.7", "6", "7", "0.7", "0.3"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDEndcapHits"],
                            "OutputCollection": ["VXDEndcapHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

OverlayFull = MarlinProcessorWrapper("OverlayFull")
OverlayFull.OutputLevel = INFO
OverlayFull.ProcessorType = "OverlayTimingRandomMix"
OverlayFull.Parameters = {
    "PathToMuPlus": [the_args.OverlayFullPathToMuPlus],
    "PathToMuMinus": [the_args.OverlayFullPathToMuMinus],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MergeMCParticles": ["false"],
    "NumberBackground": [the_args.OverlayFullNumberBackground]
}

OverlayIP = MarlinProcessorWrapper("OverlayIP")
OverlayIP.OutputLevel = INFO
OverlayIP.ProcessorType = "OverlayTimingGeneric"
OverlayIP.Parameters = {
    "AllowReusingBackgroundFiles": ["true"],
    "BackgroundFileNames": [the_args.OverlayIPBackgroundFileNames],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "Delta_t": ["10000"],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MCPhysicsParticleCollectionName": ["MCPhysicsParticles_IP"],
    "MergeMCParticles": ["true"],
    "NBunchtrain": ["1"],
    "NumberBackground": [the_args.OverlayIPNumberBackground],
    "PhysicsBX": ["1"],
    "Poisson_random_NOverlay": ["false"],
    "RandomBx": ["false"],
    "StartBackgroundFileIndex": ["0"],
    "TPCDriftvelocity": ["0.05"]
}

ClusterFilter_VBLoose = MarlinProcessorWrapper("ClusterFilter_VBLoose")
ClusterFilter_VBLoose.OutputLevel = INFO
ClusterFilter_VBLoose.ProcessorType = "FilterClusters"
ClusterFilter_VBLoose.Parameters = {
    "ThetaRanges": ["0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2"],
    "ClusterSize": ["6","5","4","5","6","7","6","5","6","7","5","5","4","5","5","5","5","4","5","5","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4"],
    "ThetaBins": ["6"],
    "Layers": ["0","1","2","3","4","5","6","7"],
    "InTrackerHitCollection": ["VXDBarrelHits_HTF"],
    "InRelationCollection": ["VXDBarrelHitsRelations_HTF"],
    "InSimTrackerHitCollection": ["VertexBarrelCollection_HTF"],
    "OutTrackerHitCollection": ["VXDBarrelHits"],
    "OutRelationCollection": ["VXDBarrelHitsRelations"],
    "OutSimTrackerHitCollection": ["VertexBarrelCollection_CF"],
    "FillHistograms": ["true"]
}

ClusterFilter_VELoose = MarlinProcessorWrapper("ClusterFilter_VELoose")
ClusterFilter_VELoose.OutputLevel = INFO
ClusterFilter_VELoose.ProcessorType = "FilterClusters"
ClusterFilter_VELoose.Parameters = {
    "ThetaRanges": ["0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2"],
    "ClusterSize": ["4","5","0","5","4","4","5","0","5","4","4","5","0","5","4","4","5","0","5","4","4","0","0","0","4","4","0","0","0","4","4","0","0","0","4","4","0","0","0","4"],
    "ThetaBins": ["6"],
    "Layers": ["0","1","2","3","4","5","6","7"],
    "InTrackerHitCollection": ["VXDEndcapHits_HTF"],
    "InRelationCollection": ["VXDEndcapHitsRelations_HTF"],
    "InSimTrackerHitCollection": ["VertexEndcapCollection_HTF"],
    "OutTrackerHitCollection": ["VXDEndcapHits"],
    "OutRelationCollection": ["VXDEndcapHitsRelations"],
    "OutSimTrackerHitCollection": ["VertexEndcapCollection_CF"],
    "FillHistograms": ["true"]
}

ClusterFilter_IBLoose = MarlinProcessorWrapper("ClusterFilter_IBLoose")
ClusterFilter_IBLoose.OutputLevel = INFO
ClusterFilter_IBLoose.ProcessorType = "FilterClusters"
ClusterFilter_IBLoose.Parameters = {
    "ThetaRanges": ["0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2","0","0.7","1.0","2.0","2.3","3.2"],
    "ClusterSize": ["4","4","3","4","4","3","3","3","3","3","3","3","3","3","3"],
    "ThetaBins": ["6"],
    "Layers": ["0","1","2"],
    "InTrackerHitCollection": ["ITBarrelHits_HTF"],
    "InRelationCollection": ["ITBarrelHitsRelations_HTF"],
    "InSimTrackerHitCollection": ["InnerTrackerBarrelCollection_HTF"],
    "OutTrackerHitCollection": ["ITBarrelHits"],
    "OutRelationCollection": ["ITBarrelHitsRelations"],
    "OutSimTrackerHitCollection": ["InnerTrackerBarrelCollection_CF"],
    "FillHistograms": ["true"]
}

ClusterFilter_IELoose = MarlinProcessorWrapper("ClusterFilter_IELoose")
ClusterFilter_IELoose.OutputLevel = INFO
ClusterFilter_IELoose.ProcessorType = "FilterClusters"
ClusterFilter_IELoose.Parameters = {
    "ThetaRanges": ["0","0.7","2.3","3.2","0","0.7","2.3","3.2","0","0.7","2.3","3.2"],
    "ClusterSize": ["3","0","3","3","0","3","3","0","3"],
    "ThetaBins": ["4"],
    "Layers": ["0","1","2"],
    "InTrackerHitCollection": ["ITEndcapHits_HTF"],
    "InSimTrackerHitCollection": ["InnerTrackerEndcapCollection_HTF"],
    "InRelationCollection": ["ITEndcapHitsRelations_HTF"],
    "OutTrackerHitCollection": ["ITEndcapHits"],
    "OutRelationCollection": ["ITEndcapHitsRelations"],
    "OutSimTrackerHitCollection": ["InnerTrackerEndcapCollection_CF"],
    "FillHistograms": ["true"]
}

ClusterFilter_OBLoose = MarlinProcessorWrapper("ClusterFilter_OBLoose")
ClusterFilter_OBLoose.OutputLevel = INFO
ClusterFilter_OBLoose.ProcessorType = "FilterClusters"
ClusterFilter_OBLoose.Parameters = {
    "ThetaRanges": ["0","0.7","1.05","2.1","2.5","3.2","0","0.7","1.05","2.1","2.5","3.2","0","0.7","1.05","2.1","2.5","3.2"],
    "ClusterSize": ["3","3","3","3","3","3","3","3","3","3","3","3","3","3","3"],
    "ThetaBins": ["6"],
    "Layers": ["0","1","2"],
    "InTrackerHitCollection": ["OTBarrelHits_HTF"],
    "InRelationCollection": ["OTBarrelHitsRelations_HTF"],
    "InSimTrackerHitCollection": ["OuterTrackerBarrelCollection_HTF"],
    "OutTrackerHitCollection": ["OTBarrelHits"],
    "OutRelationCollection": ["OTBarrelHitsRelations"],
    "OutSimTrackerHitCollection": ["OuterTrackerBarrelCollection_CF"],
    "FillHistograms": ["true"]
}

if (not the_args.doTrkDigiSimple):
    if (not the_args.doClusterFilter):
        labelTrkDigiCollection=""
    else:
        labelTrkDigiCollection="_HTF" #Hit-Time filter

HitTimeFilter_VXB = MarlinProcessorWrapper("HitTimeFilter_VXB")
HitTimeFilter_VXB.OutputLevel = INFO
HitTimeFilter_VXB.ProcessorType = "FilterTimeHits"
HitTimeFilter_VXB.Parameters = {
    "TrackerHitInputCollections": ["VXDBarrelHits_realDigi"],
    "TrackerSimHitInputCollections": ["VertexBarrelCollection"],
    "TrackerHitInputRelations": ["VXDBarrelHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["VXDBarrelHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["VertexBarrelCollection_HTF"],
    "TrackerHitOutputRelations": ["VXDBarrelHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.09"],
    "TimeUpperLimit": ["0.15"],
    "FillHistograms": ["true"]
}

HitTimeFilter_VXE = MarlinProcessorWrapper("HitTimeFilter_VXE")
HitTimeFilter_VXE.OutputLevel = INFO
HitTimeFilter_VXE.ProcessorType = "FilterTimeHits"
HitTimeFilter_VXE.Parameters = {
    "TrackerHitInputCollections": ["VXDEndcapHits_realDigi"],
    "TrackerSimHitInputCollections": ["VertexEndcapCollection"],
    "TrackerHitInputRelations": ["VXDEndcapHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["VXDEndcapHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["VertexEndcapCollection_HTF"],
    "TrackerHitOutputRelations": ["VXDEndcapHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.09"],
    "TimeUpperLimit": ["0.15"],
    "FillHistograms": ["true"]
}

HitTimeFilter_ITB = MarlinProcessorWrapper("HitTimeFilter_ITB")
HitTimeFilter_ITB.OutputLevel = INFO
HitTimeFilter_ITB.ProcessorType = "FilterTimeHits"
HitTimeFilter_ITB.Parameters = {
    "TrackerHitInputCollections": ["ITBarrelHits_realDigi"],
    "TrackerSimHitInputCollections": ["InnerTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["ITBarrelHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["ITBarrelHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["InnerTrackerBarrelCollection_HTF"],
    "TrackerHitOutputRelations": ["ITBarrelHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.18"],
    "TimeUpperLimit": ["0.3"],
    "FillHistograms": ["true"]
}

HitTimeFilter_ITE = MarlinProcessorWrapper("HitTimeFilter_ITE")
HitTimeFilter_ITE.OutputLevel = INFO
HitTimeFilter_ITE.ProcessorType = "FilterTimeHits"
HitTimeFilter_ITE.Parameters = {
    "TrackerHitInputCollections": ["ITEndcapHits_realDigi"],
    "TrackerSimHitInputCollections": ["InnerTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["ITEndcapHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["ITEndcapHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["InnerTrackerEndcapCollection_HTF"],
    "TrackerHitOutputRelations": ["ITEndcapHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.18"],
    "TimeUpperLimit": ["0.3"],
    "FillHistograms": ["true"]
}


HitTimeFilter_OTB = MarlinProcessorWrapper("HitTimeFilter_OTB")
HitTimeFilter_OTB.OutputLevel = INFO
HitTimeFilter_OTB.ProcessorType = "FilterTimeHits"
HitTimeFilter_OTB.Parameters = {
    "TrackerHitInputCollections": ["OTBarrelHits_realDigi"],
    "TrackerSimHitInputCollections": ["OuterTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["OTBarrelHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["OTBarrelHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["OuterTrackerBarrelCollection_HTF"],
    "TrackerHitOutputRelations": ["OTBarrelHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.18"],
    "TimeUpperLimit": ["0.3"],
    "FillHistograms": ["true"]
}

HitTimeFilter_OTE = MarlinProcessorWrapper("HitTimeFilter_OTE")
HitTimeFilter_OTE.OutputLevel = INFO
HitTimeFilter_OTE.ProcessorType = "FilterTimeHits"
HitTimeFilter_OTE.Parameters = {
    "TrackerHitInputCollections": ["OTEndcapHits_realDigi"],
    "TrackerSimHitInputCollections": ["OuterTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["OTEndcapHitsRelations_realDigi"],
    "TrackerHitOutputCollections": ["OTEndcapHits"+labelTrkDigiCollection],
    "TrackerSimHitOutputCollections": ["OuterTrackerEndcapCollection_HTF"],
    "TrackerHitOutputRelations": ["OTEndcapHitsRelations"+labelTrkDigiCollection],
    "TimeLowerLimit": ["-0.18"],
    "TimeUpperLimit": ["0.3"],
    "FillHistograms": ["true"]
}

algList.append(AIDA)
algList.append(EventNumber)
algList.append(DD4hep)
if the_args.doOverlayFull:
    algList.append(OverlayFull)   # Full BX BIB overlay
if the_args.doOverlayIP:
    algList.append(OverlayIP)     # Incoherent pairs full BX BIB overlay

if (the_args.doTrkDigiSimple):
    # check that filters needing full digi are not enabled
    if the_args.doClusterFilter:
        print("Cluster filter only to be applied only on realistic digitization. Please re-run without the option --doClusterFilter.")
        exit()

    # schedule simplified digitization processors
    algList.append(VXDBarrelDigitiser)
    algList.append(VXDEndcapDigitiser)
    algList.append(ITBarrelDigitiser)
    algList.append(ITEndcapDigitiser)
    algList.append(OTBarrelDigitiser)
    algList.append(OTEndcapDigitiser)

else:
    # schedule realistic digitization
    algList.append(VXDBarrelRealisticDigi)
    algList.append(VXDEndcapRealisticDigi)
    algList.append(InnerPlanarRealisticDigi)
    algList.append(InnerEndcapRealisticDigi)
#    algList.append(OuterPlanarRealisticDigi)
    algList.append(OTBarrelDigitiser)
    algList.append(OTEndcapDigitiser)

    # schedule time-based cluster filters
    algList.append(HitTimeFilter_VXB)
    algList.append(HitTimeFilter_VXE)
    #algList.append(HitTimeFilter_ITB)
    #algList.append(HitTimeFilter_ITE)
    #algList.append(HitTimeFilter_OTB)    
    #algList.append(HitTimeFilter_OTE)
    
    if the_args.doClusterFilter:
        # schedule shape-based cluster filters
        algList.append(ClusterFilter_VBLoose)
        algList.append(ClusterFilter_VELoose)
#        algList.append(ClusterFilter_IBLoose)
#        algList.append(ClusterFilter_IELoose)
#        algList.append(ClusterFilter_OBLoose)           

if the_args.doFilterDL:    
    algList.append(FilterDL_VXDB)
    algList.append(FilterDL_VXDE)

algList.append(ECalBarrelDigi)
algList.append(ECalBarrelReco)
algList.append(ECalPlugDigi)
algList.append(ECalPlugReco)
algList.append(ECalEndcapDigi)
algList.append(ECalEndcapReco)
algList.append(HCalBarrelDigi)
algList.append(HCalBarrelReco)
algList.append(HCalEndcapDigi)
algList.append(HCalEndcapReco)
algList.append(HCalRingDigi)
algList.append(HCalRingReco)
algList.append(MuonDigitiser)

    
if the_args.writeAll:
    algList.append(LCIOWriter_all)
else:
    if the_args.doClusterFilter:
        LCIOWriter_light.Parameters["DropCollectionNames"]=["VXDBarrelHits_HTF", "VXDEndcapHits_HTF", "ITBarrelHits_HTF", "ITEndcapHits_HTF", "OTBarrelHits_HTF", "OTEndcapHits_HTF", "VXDBarrelHits_realDigi", "VXDEndcapHits_realDigi", "ITBarrelHits_realDigi", "ITEndcapHits_realDigi", "OTBarrelHits_realDigi", "OTEndcapHits_realDigi", "VertexBarrelCollection_HTF", "VertexEndcapCollection_HTF", "InnerTrackerBarrelCollection_HTF", "InnerTrackerEndcapCollection_HTF", "OuterTrackerBarrelCollection_HTF", "OuterTrackerEndcapCollection_HTF"]
    algList.append(LCIOWriter_light)

#from k4FWCore import ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )
#                EvtMax   = 10,
