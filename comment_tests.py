import unittest
from data_transformation import extract_wait_time_and_oxygen


class CommentExtractTest(unittest.TestCase):

    # Test with wait time present but not liters
    def test1(self):
        input = "Wait time: 0 minutes//Dx Suicidal ideation // Height 5'1 // Weight 186 pounds// None//H: 5'1 W:186 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Removed numbers from wait time and liters
    def test2(self):
        input = "Wait time: minutes//Dx Suicidal ideation // Height 5'1 // Weight 186 pounds// None//H: 5'1 W:186 lbs. liters"
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # No wait time or no liters present in string - maniupl
    def test3(self):
        input = "Dx Suicidal ideation // Height 5'1 // Weight 186 pounds// None//H: 5'1 W:186 lbs"
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Has wait time and minutes, but has extraneous quotation marks present. Manipulated original string to have the escape character before the quotation mark from the end of the string
    def test4(self):
        input = "Wait time: 0 minutes//Height 4'11 /// Weight 138 lbs./// Vent  FiO2 30% /// Oxygen 8L //respiratory therapist// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs.\""
        expected = [0, 8]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test5(self):
        input = "Wait time: 0 minutes//DX - weakness / WT -300  lbs.  Ht -5.7  Stairs - 0  COVID-19 - Neg Monkey pox - Neg// Bariatric//H: 6'0 W:361 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test6(self):
        input = "Wait time: 0 minutes//Height 4'11 /// Weight 138 lbs./// Vent  FiO2 30% /// Oxygen 8L //respiratory therapist// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs."
        expected = [0, 8]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if text contains oxygen, set to 2
    def test7(self):
        input = "Wait time: 0 minutes//// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test8(self):
        input = "Wait time: 90 minutes//Respiratory failure// Please make sure you assigned bariatric 8 L OF OXYGEN // Oxygen//Bariatric//Wait4Return//G Tube//Deep suction//Resp Therapist REQ//H: 5'3 W:300 lbs."
        expected = [90, 8]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if text contains oxygen, set to 2
    def test9(self):
        input = "Wait time: 0 minutes//// Oxygen//Bariatric//Wait4Return//G Tube//Deep suction//Resp Therapist REQ//H: 5'3 W:300 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test10(self):
        input = "Wait time: 0 minutes//DX abdominal pain// height 5'6ft weight 150lbs// ER Room 1 Wall// has cane// covid negative// ETA CALL 818-252-2184// Cane//Call Upon Arrival//H: 5'6 W:150 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test11(self):
        input = "Wait time: 90 minutes//Oxygen 1L Deep suction /Height 5'4  Weight 147 lbs. DX- respiratory failure// Oxygen//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 5'4 W:147 lbs.\""
        expected = [90, 1]

    # if text contains oxygen, set to 2
    def test12(self):
        input = "Wait time: 0 minutes//// Oxygen//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 5'4 W:147 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test13(self):
        input = "Wait time: 0 minutes//DX ESRD// None//H: 5'5 W:110 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test14(self):
        input = "Wait time: 0 minutes//// None//H: 5'5 W:110 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test15(self):
        input = "Wait time: 0 minutes//Dx: Acute and respiratory failure//Height 4'8  Weight 112 lbs.//RT on board //TBAR 2 LITERS// Deep suction//Resp Therapist REQ//H: 4'8 W:112 lbs.\""
        expected = [0, 2]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test16(self):
        input = "Wait time: 0 minutes//// Deep suction//Resp Therapist REQ//H: 4'8 W:112 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test17(self):
        input = "Wait time: 0 minutes//Traumatic brain injury// // Vent//Resp Therapist REQ//Trach Tube//H: 5'8 W:124 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test18(self):
        input = "Wait time: 0 minutes//Traumatic brain injury// // Vent//Resp Therapist REQ//Trach Tube//H: 5'8 W:124 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test19(self):
        input = "Wait time: 0 minutes//Traumatic brain injury// // Vent//Resp Therapist REQ//Trach Tube//H: 5'8 W:124 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test20(self):
        input = "Wait time: 0 minutes//// Vent//Resp Therapist REQ//Trach Tube//H: 5'8 W:124 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test21(self):
        input = "Wait time: 0 minutes//// Vent//Resp Therapist REQ//Trach Tube//H: 5'8 W:124 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # lts
    def test22(self):
        input = "Wait time: 90 minutes//Dx Respiratoy failure ; 2 lts Oxygen //tracheostomy -RT NEEDED Due to deep suction //  Height 6'2  Weight 182 lbs.// Preferred Vendor Ambiance ambulance // 90 wait and return// Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 6'2 W:182 lbs.\""
        expected = [90, 2]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test23(self):
        input = "Wait time: 0 minutes//1st Fl ; admitting Dpt // // Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 6'2 W:182 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test24(self):
        input = "Wait time: 0 minutes//Dx: chronic respiratory failure; vent with FiO2 of 32%; Height 5'  Weight 91 lbs.// Vent//Resp Therapist REQ//Trach Tube//H: 5'2 W:110 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test25(self):
        input = "Wait time: 0 minutes//received by medical staff// Vent//Resp Therapist REQ//Trach Tube//H: 5'2 W:110 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test26(self):
        input = "Wait time: 0 minutes//BLS / DX: Hypotension /Post OP vaginal bleeding / ER Bed 16 /// None//H: 5'4 W:190 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test27(self):
        input = "Wait time: 0 minutes//DX: Foreign body on throat// H: 6'0 W: 338 Lbs // Steps: 0// Cardiac monitor req //Veiwpoint ambulance Requested // Bariatric//Cardiac Monitor//H: 5'6 W:338 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # if contain Resp Therapist REQ, set to 15lpm?
    def test28(self):
        input = "Wait time: 0 minutes//DX- anoxit brain height 5:6; weight 117 lbs; ST 3// Vent//None//Resp Therapist REQ//H: 5'7 W:117 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test29(self):
        input = "Wait time: 0 minutes//Height 5'5  Weight 134 lbs| Dx: she is alter - dementia// 5150 Hold//Stair Chair//H: 5'5 W:134 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time and and lt present in string
    def test30(self):
        input = "Wait time: 90 minutes//there is a flat entrance //Height 4'11 Weight 120 lbs./Fio2 3 lt of oxygen via trach // 661 - 400 - 7684 DORIS - NURSE/CARETAKER// Vent//Deep suction//Resp Therapist REQ//Trach Tube//H: 4'11 W:120 lbs.\""
        expected = [90, 3]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present without oxygen
    def test31(self):
        input = "Wait time: 0 minutes//// Vent//Deep suction//Resp Therapist REQ//Trach Tube//H: 4'11 W:120 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with unspecified number for oxygen
    def test32(self):
        input = "Wait time: 0 minutes//suite 200 // (323) 663-3333 no steps// Oxygen//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 5'7 W:216 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with number after oxygen and before liters
    def test33(self):
        input = "Wait time: 0 minutes//Height 6'6  Weight 172 lbs.//Viewpoint Ambulance; Inc vendor requested// oxygen 5 liters// RT req; portable deep suction machine.// Oxygen//Deep suction//Resp Therapist REQ//H: 6'6 W:172 lbs.\""
        expected = [0, 5]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with unspecified number for oxygen
    def test34(self):
        input = "Wait time: 0 minutes//// Oxygen//Deep suction//Resp Therapist REQ//H: 6'6 W:172 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present without oxygen
    def test35(self):
        input = "Wait time: 0 minutes//Weight 125 lbs.//Height 5'4// Vent//Wait4Return//Resp Therapist REQ//Trach Tube//H: 5'4 W:125 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present without oxygen
    def test36(self):
        input = "Wait time: 0 minutes//// Vent//Wait4Return//Resp Therapist REQ//Trach Tube//H: 5'4 W:125 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with number after oxygen and before L
    def test37(self):
        input = "Wait time: 0 minutes//Height 4'11 /// Weight 138 lbs./// Vent  FiO2 30% /// Oxygen 8L //respiratory therapist// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs.\""
        expected = [0, 8]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with unspecified number for oxygen
    def test38(self):
        input = "Wait time: 0 minutes//// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with number after oxygen and before L
    def test39(self):
        input = "Wait time: 60 minutes//oxygen 2L - suctions machine | Height 3'7  Weight 36 lbs | Dx: dip dislocated ; Cerebral Pasly | wait4return // Oxygen//Wait4Return//Nonverbal//G Tube//Deep suction//Trach Tube//H: 3'7 W:36 lbs.\""
        expected = [60, 2]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present with unspecified number for oxygen
    def test40(self):
        input = "Wait time: 0 minutes//staff - no name provided // Oxygen//Wait4Return//Nonverbal//G Tube//Deep suction//Trach Tube//H: 3'7 W:36 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    # Wait time present without oxygen
    def test41(self):
        input = "Wait time: 0 minutes//dx  depresion and ensaity -covid// None//H: 5'2 W:160 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    #
    def test42(self):
        input = (
            "Wait time: 0 minutes//213 lbs 5 ft 7 / sepsis // None//H: 5'7 W:213 lbs."
        )
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test43(self):
        input = "Wait time: 0 minutes//Dx: 5150 hold with danger to herself and to other; full body restrains recommended; Height 5'  Weight 111 lbs.// 5150 Hold//H: 5' W:111 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test44(self):
        input = "Wait time: 0 minutes//DX- chest pain; height 5:6; weight 145 lbs;ST 0;// IV Drips//Cardiac Monitor//H: 5'6 W:145 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test45(self):
        input = "Wait time: 0 minutes//Height 5'9 Weight 150 lbs.// DX: RESPITORY FAILURE//// Case Managed//VIP//Vent//Resp Therapist REQ//Trach Tube//CIII//H: 5'9 W:162 lbs.\""
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test46(self):
        input = "Wait time: 0 minutes//Dx: 5150 Danger to herself/restrings/ Height 5'7  Weight 120 lbs//// 5150 Hold//H: 5'7 W:120 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test47(self):
        input = "Wait time: 0 minutes//DX ESRD// None//H: 5'5 W:110 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test48(self):
        input = "Wait time: 90 minutes//Height 6 Foot // Weight 174 // RT // Vent VT 450; PEEP PLUS 5 ; FOI2 30%// Vent//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 6' W:174 lbs."
        expected = [90, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test49(self):
        input = "Wait time: 0 minutes//// Vent//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 6' W:174 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test50(self):
        input = "Wait time: 90 minutes//DX: chronic respiratory failure  // Oxygen 5lt. // // Oxygen//Vent//Wait4Return//Resp Therapist REQ//H: 5'9 W:112 lbs."
        expected = [90, 5]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test51(self):
        input = "Wait time: 0 minutes//// Oxygen//Vent//Wait4Return//Resp Therapist REQ//H: 5'9 W:112 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test52(self):
        input = "Wait time: 0 minutes//DX: respiratory failure  // trach tube // Bariatric//WC Oversized//Trach Tube//WC Transferable//H: 6'2 W:451 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test53(self):
        input = "Wait time: 0 minutes//Dx: Cholangitis // H: 5' 4  W: 175 lbs // Resp therapist req. // Vent - FiO2: 30% ; Peep of 6// Trach tube // Deep suction // Isolation precaution// Vent//Deep suction//Resp Therapist REQ//Iso Precaution ACTIVE//Trach Tube//H: 5'4 W:175 lbs.\""
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test54(self):
        input = "Wait time: 0 minutes//Dx//mrsa esbl/ht 10 wt/190/Fio2 28% 5l O2// Oxygen//Iso Precaution ACTIVE//Trach Tube//H: 6'1 W:216 lbs."
        expected = [0, 5]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test55(self):
        input = "Wait time: 0 minutes//Dx: Acute and respiratory failure//Height 4'8  Weight 112 lbs.//RT on board //TBAR 2 LITERS// Deep suction//Resp Therapist REQ//Trach Tube//H: 4'8 W:112 lbs.\""
        expected = [0, 2]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test56(self):
        input = "Wait time: 0 minutes//// Deep suction//Resp Therapist REQ//Trach Tube//H: 4'8 W:112 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test57(self):
        input = "Wait time: 90 minutes//// Vent//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 5'0 W:115 lbs."
        expected = [90, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test58(self):
        input = "Wait time: 0 minutes//// Vent//Wait4Return//Deep suction//Resp Therapist REQ//Trach Tube//H: 5'0 W:115 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test59(self):
        input = "Wait time: 60 minutes//DX: Respiratory Failure // HT: 56in WT: 147 lbs// Resp Therapist REQ//H: 4'6 W:160 lbs."
        expected = [60, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test60(self):
        input = "Wait time: 0 minutes//// Resp Therapist REQ//H: 4'6 W:160 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test61(self):
        input = "Wait time: 60 minutes// VENT FiO2  21% /// Height 38 INCHES /////  Weight 182. KILOS  // Respiratory therapist // Vent//Wait4Return//Escort Required//Deep suction//Resp Therapist REQ//Trach Tube//H: 3'1 W:40 lbs."
        expected = [60, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test62(self):
        input = "Wait time: 0 minutes//// Vent//Wait4Return//Escort Required//Deep suction//Resp Therapist REQ//Trach Tube//H: 3'1 W:40 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test63(self):
        input = "Wait time: 240 minutes//Height 4'11 /// Weight 138 lbs./// Vent  FiO2 30% /// Oxygen 8L //respiratory therapist// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs.\""
        expected = [240, 8]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test64(self):
        input = "Wait time: 0 minutes//// Oxygen//Vent//Resp Therapist REQ//Trach Tube//H: 4'11 W:138 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test65(self):
        input = "Wait time: 0 minutes//// Vent//None//Wait4Return//H: 5'0 W:122 lbs."
        expected = [0, None]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test66(self):
        input = "Wait time: 0 minutes//5 ft 6 160 lbs /  danger to self.// None//H: 5'6 W:160 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test67(self):
        input = "Wait time: 0 minutes//DX: blood pressure; hypertension //Height 5'10  //Weight 212 lbs.// 5150 Hold//H: 5'10 W:212 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test68(self):
        input = "Wait time: 0 minutes//Dx danger to self 5150 //full body restrains// Height 5'6 //  Weight 130 lbs.// 5150 Hold//H: 5'6 W:130 lbs.\""
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test69(self):
        input = "Wait time: 0 minutes//DX: 5150 Hold danger to self // Full body Restraints// 5150 Hold//H: 5'9 W:160 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)

    def test70(self):
        input = "Wait time: 0 minutes//DX: 5150 hold / DTS DTO Restraints Required / HT: 5'8 WT: 188LBS / Rm ED 21-A / preferred vendor: Viewpoint Ambulance; Inc// 5150 Hold//H: 5'8 W:188 lbs."
        expected = [0, 0]
        self.assertEqual(extract_wait_time_and_oxygen(input), expected)


if __name__ == "__main__":
    unittest.main()
