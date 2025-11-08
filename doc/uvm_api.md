
# UVM API TODO List

## uvm_object
* reseed
* set_name
* get_name
* get_full_name
* get_inst_id
* get_inst_count
x get_type
* get_type_name
* create
* clone
* print (omit 'printer' parameter)
* sprint (omit 'printer' parameter)
* convert2string
* record (omit 'recorder' parameter)
* copy
* compare
* set_int_local (use int as value)
* set_string_local
* set_object_local

## uvm_phase
- raise_objection
- drop_objection

## uvm_component
- get_parent
- get_child
- lookup
- get_depth

## uvm_component_proxy
x end_of_elaboration_phase (exp)
x start_of_simulation_phase (exp)
x run_phase (exp)
x pre_reset_phase (exp)
x reset_phase (exp)
x post_reset_phase (exp)
x pre_configure_phase (exp)
x configure_phase (exp)
x post_configure_phase (exp)
x pre_main_phase (exp)
x main_phase (exp)
x post_main_phase (exp)
x pre_shutdown_phase (exp)
x shutdown_phase (exp)
x post_shutdown_phase (exp)
x extract_phase (exp)
x check_phase (exp)
x report_phase (exp)
x final_phase (exp)
x phase_start (exp)
x phase_ready_to_end (exp)
x phase_ended (exp)

