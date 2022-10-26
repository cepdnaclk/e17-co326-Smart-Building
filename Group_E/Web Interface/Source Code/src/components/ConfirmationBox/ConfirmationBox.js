import React from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";


export default function ConfirmationBox({
                                            open,
                                            id,
                                            title,
                                            handleClose,
                                            deleteSchedule,
                                        }) {
    return (
        <div>
            <Dialog
                open={open}
                onClose={handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                    <div id="alert-dialog-title" className="confirm_ pt-20 pl-50 pr-50">
                        {"Do you want to delete schedule named " + title + " ?"}
                    </div>

                    <DialogActions className="pl-50 pr-50">

                        <Button onClick={handleClose} color="primary">
                            <span className="confirm_button_">
                                No
                            </span>

                        </Button>
                        <Button
                            onClick={deleteSchedule.bind(null, id)}
                            color="primary"
                            autoFocus
                        >
                             <span className="confirm_button_">
                                Yes
                            </span>
                        </Button>
                    </DialogActions>
            </Dialog>
        </div>
    );
}
