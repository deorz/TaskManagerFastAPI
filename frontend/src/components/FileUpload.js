import Button from "@mui/material/Button";
import { Divider, Stack } from "@mui/material";
import Typography from "@mui/material/Typography";

function FileUpload(props) {
    const handleFileChange = (e) => {
        if (e.target.files) {
            let fileObject = {
                name: e.target.files[0].name,
                mimetype: e.target.files[0].type,
                body: "",
            }
            let reader = new FileReader();
            reader.readAsDataURL(e.target.files[0]);
            reader.onload = async () => {
                fileObject.body = await reader.result;
            };
            props.setFile(fileObject);
        }
    };
    return (
        <>
            <input
                className="classes.input"
                style={{ display: 'none' }}
                id="file"
                multiple
                type="file"
                onChange={handleFileChange}
                accept=".py"
            />
            <label htmlFor="file">
                <Stack direction="row" spacing={2} divider={<Divider orientation="vertical" flexItem />}>
                    <Button
                        color="primary"
                        variant="contained"
                        component="span"
                        className="classes.button"
                        sx={{width: '49%'}}
                    >
                        Прикрепить
                    </Button>
                    <Typography
                        variant="subtitle1"
                        sx={{ pt: 0.5, width: '49%' }}
                        align="center"
                    >{props.file && props.file.name}</Typography>
                </Stack>
            </label>
        </>
    );
}

export default FileUpload;
