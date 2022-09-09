## module quantic gui logic
'''
Module to contain logic checks of controls
'''


def set_prop(gui_inf):
    '''
    Control which options are allowed when propagation level options get set
    gui_inf is the UI interface
    '''
    if gui_inf.levels["lev1_rad"].isChecked():
        #only level 1 control can be checked
        #set level 1
        gui_inf.levels["gendvr_chk"].setCheckable(True)
        #blank level 2
        gui_inf.levels["genoper_chk"].setChecked(False)
        gui_inf.levels["genpes_chk"].setChecked(False)

        gui_inf.levels["genoper_chk"].setCheckable(False)
        gui_inf.levels["genpes_chk"].setCheckable(False)

        #blank level 3
        gui_inf.levels["geninwf_chk"].setChecked(False)

        gui_inf.levels["geninwf_chk"].setCheckable(False)
        #blank level 4

        gui_inf.levels["prop_rad"].setCheckable(False)
        gui_inf.levels["cont_rad"].setCheckable(False)
        gui_inf.levels["test_rad"].setCheckable(False)
        gui_inf.levels["rel_rad"].setCheckable(False)

        gui_inf.levels["prop_rad"].setChecked(False)
        gui_inf.levels["cont_rad"].setChecked(False)
        gui_inf.levels["test_rad"].setChecked(False)
        gui_inf.levels["rel_rad"].setChecked(False)

        gui_inf.update()
        # self.levels["lev2_rad"].setChecked(False)
        # self.levels["lev3_rad"].setChecked(False)
        # self.levels["lev4_rad"].setChecked(False)

    elif gui_inf.levels["lev2_rad"].isChecked():
    #     #only level 2 controls checked
        #only level 1 control can be checked
        #set level 1
        gui_inf.levels["gendvr_chk"].setCheckable(False)
        #blank level 2
        gui_inf.levels["genoper_chk"].setChecked(False)
        gui_inf.levels["genpes_chk"].setChecked(False)

        gui_inf.levels["genoper_chk"].setCheckable(True)
        gui_inf.levels["genpes_chk"].setCheckable(True)

        #blank level 3
        gui_inf.levels["geninwf_chk"].setChecked(False)

        gui_inf.levels["geninwf_chk"].setCheckable(False)
        #blank level 4
        gui_inf.levels["prop_rad"].setChecked(False)
        gui_inf.levels["cont_rad"].setChecked(False)
        gui_inf.levels["test_rad"].setChecked(False)
        gui_inf.levels["rel_rad"].setChecked(False)

        gui_inf.levels["prop_rad"].setCheckable(False)
        gui_inf.levels["cont_rad"].setCheckable(False)
        gui_inf.levels["test_rad"].setCheckable(False)
        gui_inf.levels["rel_rad"].setCheckable(False)

        gui_inf.update()
    elif gui_inf.levels["lev3_rad"].isChecked():
    #     #only level 3 controls checked
        #only level 1 control can be checked
        #set level 1
        gui_inf.levels["gendvr_chk"].setCheckable(False)
        #blank level 2
        gui_inf.levels["genoper_chk"].setChecked(False)
        gui_inf.levels["genpes_chk"].setChecked(False)

        gui_inf.levels["genoper_chk"].setCheckable(False)
        gui_inf.levels["genpes_chk"].setCheckable(False)

        #blank level 3
        gui_inf.levels["geninwf_chk"].setChecked(False)

        gui_inf.levels["geninwf_chk"].setCheckable(True)
        #blank level 4
        gui_inf.levels["prop_rad"].setChecked(False)
        gui_inf.levels["cont_rad"].setChecked(False)
        gui_inf.levels["test_rad"].setChecked(False)
        gui_inf.levels["rel_rad"].setChecked(False)

        gui_inf.levels["prop_rad"].setCheckable(False)
        gui_inf.levels["cont_rad"].setCheckable(False)
        gui_inf.levels["test_rad"].setCheckable(False)
        gui_inf.levels["rel_rad"].setCheckable(False)

        gui_inf.update()

    elif gui_inf.levels["lev4_rad"].isChecked():
    #     #only level 4 controls checked
        #only level 1 control can be checked
        #set level 1
        gui_inf.levels["gendvr_chk"].setCheckable(False)
        #blank level 2
        gui_inf.levels["genoper_chk"].setChecked(False)
        gui_inf.levels["genpes_chk"].setChecked(False)

        gui_inf.levels["genoper_chk"].setCheckable(False)
        gui_inf.levels["genpes_chk"].setCheckable(False)

        #blank level 3
        gui_inf.levels["geninwf_chk"].setChecked(False)

        gui_inf.levels["geninwf_chk"].setCheckable(False)
        #blank level 4
        gui_inf.levels["prop_rad"].setChecked(False)
        gui_inf.levels["cont_rad"].setChecked(False)
        gui_inf.levels["test_rad"].setChecked(False)
        gui_inf.levels["rel_rad"].setChecked(False)

        gui_inf.levels["prop_rad"].setCheckable(True)
        gui_inf.levels["cont_rad"].setCheckable(True)
        gui_inf.levels["test_rad"].setCheckable(True)
        gui_inf.levels["rel_rad"].setCheckable(True)

        gui_inf.update()