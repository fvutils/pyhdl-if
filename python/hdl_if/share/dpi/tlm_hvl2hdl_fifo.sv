
interface tlm_hvl2hdl_fifo #(
    parameter Twidth=32, 
    parameter Tdepth=1) (
    input               clock,
    input               reset,
    output              valid,
    input               ready,
    output[Twidth-1:0]  dat_o);
    import pyhdl_if::*;
    localparam pointer_w = (Tdepth > 1)?$clog2(Tdepth):1;
    localparam counter_w = pointer_w+1;

    reg[Twidth-1:0]     fifo[Tdepth-1:0];
    reg[pointer_w-1:0]  rptr;
    reg[pointer_w-1:0]  wptr;
    reg[counter_w-1:0]  count;

    assign valid = (count != 0);
    assign dat_o = fifo[rptr];

    wire pop = (valid && ready);
    reg                 push;
    reg[Twidth-1:0]     push_dat;

    always @(posedge clock or posedge reset) begin
        if (reset) begin
            rptr <= {pointer_w{1'b0}};
            wptr <= {pointer_w{1'b0}};
            count <= {counter_w{1'b0}};
            push = 0;
        end else begin
            case ({push, pop})
            2'b00: begin end
            2'b01: begin // Pop with no push
                count <= count - 1;
                rptr <= ((rptr+1) & (Tdepth-1));
            end
            2'b10: begin // Push with no pop
                fifo[wptr] <= push_dat;
                count <= count + 1;
                wptr <= ((wptr+1) & (Tdepth-1));
                push = 0;
            end
            2'b11: begin // Simultaneous push and pop
                fifo[wptr] <= push_dat;
                wptr <= ((wptr+1) & (Tdepth-1));
                rptr <= ((rptr+1) & (Tdepth-1));
                push = 0;
            end
            endcase
        end
    end

    task put(input reg[Twidth-1:0]  dat);
        while (reset !== 0) begin
            @(posedge clock);
        end

        while (push == 1) begin
            @(posedge clock);
        end

        push = 1'b1;
        push_dat = dat;

        // Wait to take effect
    endtask

    class Closure implements ICallApi;

        virtual function PyObject invokeFunc(
            string      method,
            PyObject    args);
            $display("Fatal Error: unexpected function invocation %0s", method);
            $finish;
        endfunction

        virtual task invokeTask(
            output PyObject    retval,
            input string       method,
            input PyObject     args);
            bit [Twidth-1:0]    tmp = 0;
            PyObject obj, intval, rshift;

            $display("invokeTask: method=%0s", method);

            retval = None;

            case (method)
                "put": begin
                    intval = PyTuple_GetItem(args, 0);

                    if (Twidth <= 64) begin
                        longint unsigned lval;
                        lval = PyLong_AsUnsignedLongLong(intval);
                        tmp = lval[Twidth-1:0];
                    end else begin
                        rshift = PyObject_GetAttrString(intval, "__rshift__");
                        $display("TODO: implement >64-bit");
                        $finish;
                    end
                    put(tmp); 
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
            StreamKind_Req,
            $sformatf("%m"),
            __closure);
    end


endinterface
