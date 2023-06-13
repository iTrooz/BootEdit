from bootedit.backend.backend import Backend

class TestBackend(Backend):

    def get_uefi_entries(self) -> list[str]:
        return ["Windows Boot Manager", "GRUB", "Removable USB device", "Network boot"]
