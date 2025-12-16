/**
 * pyhdl_uvm_type_rgy.svh
 *
 * Copyright 2024 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */

typedef class via_uvm_component_factory;
typedef class via_uvm_object_factory;
typedef class via_uvm_object_type;
typedef class via_uvm_sequence_factory;
typedef class via_uvm_sequencer;

class factory_print_catcher extends uvm_report_catcher;
    string  factory_print;

    function new(string name="factory_print_catcher");
        super.new(name);
    endfunction

    //This example demotes "MY_ID" errors to an info message
    function action_e catch();
        factory_print = get_message();

        // Suppress the message
        return CAUGHT;
    endfunction
endclass

class via_uvm_type_rgy;
    static via_uvm_type_rgy     m_inst;
    via_uvm_object_type         m_obj_type_m[uvm_object_wrapper];

    function void init();
        factory_print_catcher catcher = new;
        uvm_factory factory = uvm_factory::get();
//        custom_report_server custom = new();

        // Attach our custom report catcher so we can 
        // save the message printed by factory.print()
        uvm_report_cb::add(null, catcher);

        `PYHDL_IF_DEBUG(("--> print"))
        factory.print();
        `PYHDL_IF_DEBUG(("<-- print\n%0s", catcher.factory_print))

        uvm_report_cb::delete(null, catcher);
    endfunction

    virtual function via_uvm_object_type get_object_type(uvm_object obj);
        uvm_object_wrapper t = obj.get_object_type();
        via_uvm_object_type t_if;

        if (m_obj_type_m.exists(t)) begin
            t_if = m_obj_type_m[t];
        end else begin
            // Build a new one
            t_if = create_obj_type(obj);

            m_obj_type_m[t] = t_if;
        end

        return t_if;
    endfunction

    virtual function via_uvm_object create(uvm_object obj);
        via_uvm_object_type obj_t = get_object_type(obj);
        via_uvm_object ret = obj_t.create(obj);
        return ret;
    endfunction

    function via_uvm_object_type create_obj_type(uvm_object obj);
        uvm_component comp;
        uvm_sequence_base seq;
        via_uvm_object_type t_if;

`ifdef XILINX_SIMULATOR
        // xsim appears to have poor support for dynamic casts. 
        // we use the UVM-defined typename instead
        begin
            string tn = obj.get_type_name();
            if (tn == "uvm_component") begin
                t_if = new(obj.get_object_type(), via_uvm_component_factory::inst(), VIA_KIND_COMPONENT);
            end else if (tn == "uvm_sequencer") begin
                t_if = new(obj.get_object_type(), via_uvm_sequencer_factory::inst(), VIA_KIND_SEQUENCER);
            end else if (tn == "uvm_sequence") begin
                t_if = new(obj.get_object_type(), via_uvm_sequence_factory::inst(), VIA_KIND_SEQUENCE);
            end else begin
                t_if = new(obj.get_object_type(), via_uvm_object_factory::inst(), VIA_KIND_OBJECT);
            end
        end
`else
        if ($cast(comp, obj)) begin
            t_if = create_comp_type(comp);
        end else if ($cast(seq, obj)) begin
            t_if = new(obj.get_object_type(), via_uvm_sequence_factory::inst(), VIA_KIND_SEQUENCE);
        end else begin
            // Just a plain UVM object
            t_if = new(obj.get_object_type(), via_uvm_object_factory::inst(), VIA_KIND_OBJECT);
        end
`endif

        if (t_if != null) begin
            populate_fields(t_if, obj.sprint());
        end

        return t_if;
    endfunction

    function via_uvm_object_type create_comp_type(uvm_component comp);
        uvm_sequencer_base seqr;
        via_uvm_object_type t_if;

        if ($cast(seqr, comp)) begin
            t_if = new(seqr.get_object_type(), via_uvm_sequencer_factory::inst(), VIA_KIND_SEQUENCER);
        end else begin
            // Just a plain component
            t_if = new(comp.get_object_type(), via_uvm_component_factory::inst(), VIA_KIND_COMPONENT);
        end

        return t_if;
    endfunction

    function void populate_fields(via_uvm_object_type t_if, string layout);
        string lines[$];
        string tokens[$];
        via_uvm_object_type cls;
        string line;
        int count;

//        `PYHDL_IF_DEBUG(("parse:\n%0s", layout))

        // Split layout into lines
        while (layout != "") begin
            int newline = strchr(layout, "\n");
            if (newline == -1) begin
                lines.push_back(layout);
                layout = "";
            end else begin
                lines.push_back(layout.substr(0, newline));
                layout = layout.substr(newline+1, layout.len()-1);
            end
        end

        // Process each line
        foreach (lines[i]) begin
            line = lines[i];

            // Skip separator lines and empty lines
            if (line.len() == 0 || line[0] == "-") continue;

            // Split line into tokens
            tokens.delete();
            while (line != "" && line[0] == " ") line = line.substr(1, line.len()-1); // Trim leading spaces
            while (line != "") begin
                int space = strchr(line, " ");
                if (space == -1) begin
                    if (line != "") tokens.push_back(line);
                    line = "";
                end else begin
                    string token = line.substr(0, space-1);
                    if (token != "") tokens.push_back(token);
                    line = line.substr(space+1, line.len()-1);
                    while (line != "" && line[0] == " ") line = line.substr(1, line.len()-1);
                end
            end

            if (count == 0) begin
                // Ignore
            end else if (count == 1) begin
                // Save type
//                `PYHDL_IF_DEBUG(("Type: %0s", tokens[1]))
            end else if (tokens.size() >= 3) begin
                // Process tokens
                string field_name = tokens[0];
                int size;

                // Distinguish string, int, list, array, object
                // Skip class line (contains "-" for size)
                if (tokens[2] == "-") continue;

                // Convert size string to integer
                size = tokens[2].atoi();

                // Create and add field
                begin
                    via_field field = new(field_name, FIELD_KIND_INT, size, 0); // Assuming unsigned for now
//                    `PYHDL_IF_DEBUG(("Field: %0s, %0d", field_name, size))
                    t_if.m_fields.push_back(field);
                end
            end
            count += 1;
        end
    endfunction

    function int strchr(string str, byte c, int start=0);
        int ret = -1;
        for (int i=start; i<str.len(); i++) begin
            if (str.getc(i) == c) begin
                ret = i;
                break;
            end
        end
        return ret;
    endfunction

    static function via_uvm_type_rgy inst();
        if (m_inst == null) begin
            m_inst = new();
            m_inst.init();
        end
        return m_inst;
    endfunction

endclass

