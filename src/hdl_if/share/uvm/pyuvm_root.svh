
class pyuvm_root extends uvm_component;
    `uvm_component_utils(pyuvm_root)
    
    // Constructor
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    // Build phase
    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        $display("Building pyuvm_root component");
        // Add any additional build tasks here
    endfunction
    
    // Connect phase
    function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        // Add any additional connection tasks here
    endfunction

endclass
