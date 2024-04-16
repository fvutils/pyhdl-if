
interface tlm_hdl2hvl_fifo #(
    parameter Twidth=32, 
    parameter Tdepth=1) (
    input               clock,
    input               reset,
    input               valid,
    output              ready,
    input[Twidth-1:0]   dat_i);
    import pyhdl_dpi_if::*;
    import pyhdl_call_if::*;
    import pyhdl_tlm_if::*;
    localparam pointer_w = (Tdepth > 1)?$clog2(Tdepth):1;
    localparam counter_w = pointer_w+1;

    reg[Twidth-1:0]     fifo[Tdepth-1:0];
    reg[pointer_w-1:0]  rptr;
    reg[pointer_w-1:0]  wptr;
    reg[counter_w-1:0]  count;

    assign ready = ((count != Tdepth) & !reset);
    wire push = (valid & ready);
    reg pop;

    always @(posedge clock or posedge reset) begin
        if (reset) begin
            rptr <= {pointer_w{1'b0}};
            wptr <= {pointer_w{1'b0}};
            count <= {counter_w{1'b0}};
            pop = 0;
        end else begin
            case ({push, pop})
            2'b01: begin // Pop with no push
                count <= count - 1;
                rptr <= ((rptr + 1) & (Tdepth-1));
                pop = 0;
            end
            2'b10: begin // Push with no pop
                fifo[wptr] <= dat_i;
                count <= count + 1;
                wptr <= ((wptr+1) & (Tdepth-1));
            end
            2'b11: begin // Simultaneous push and pop
                fifo[wptr] <= dat_i;
                wptr <= ((wptr+1) & (Tdepth-1));
                rptr <= ((rptr + 1) & (Tdepth-1));
                pop = 0;
            end
            endcase
        end
    end

    task get(output reg[Twidth-1:0] dat_o);
        while (reset !== 0) begin
            @(posedge clock);
        end

        while (count == 0 || pop == 1) begin
            @(posedge clock);
        end
        dat_o = fifo[rptr];
        pop = 1;
    endtask

    class Closure implements PyHdlCallApiIF;

        virtual function PyObject invokeFunc(
            string      method,
            PyObject    args);
            $display("Fatal Error: unexpected function invocation %0s", method);
            $finish;
        endfunction

        virtual task invokeTask(
            string      method,
            PyObject    args);
            bit [Twidth-1:0]    tmp = 0;
            case (method)
                "get": begin
                    PyObject obj = PyTuple_GetItem(args, 0);
                    PyObject fromint_m = PyObject_GetAttrString(obj, "fromint");
                    PyObject fromint_args = PyTuple_New(1);
                    PyObject intval = null;
                    get(tmp);

                    if (Twidth <= 64) begin
                        intval = PyLong_FromUnsignedLongLong(tmp);
                    end else begin
                        $display("TODO: implement >64-bit");
                        $finish;
                    end
                    PyTuple_SetItem(fromint_args, 0, intval);
                    PyObject_Call(fromint_m, fromint_args, null);
                end
                default: begin
                    $display("Fatal Error: unsupported task call %0s", method);
                    $finish;
                end
            endcase
        endtask

    endclass

    Closure             __closure;
    PyObject            __obj;

    initial begin : fifo_reg
        __closure = new();
        __obj = pyhdl_tlm_if_registerStream(
            StreamKind_Rsp,
            $sformatf("%m"),
            __closure);
    end

endinterface