import { useEffect, useRef, useState } from "react";
import Image from "next/image";

export default function ProductImageModal({
  openedImageSrc,
  setOpenedImageSrc,
}: {
  openedImageSrc: string | null;
  setOpenedImageSrc: React.Dispatch<React.SetStateAction<string | null>>;
}) {
  const imageModalRef = useRef<HTMLDialogElement>(null);

  const handleModalOutsideClose = (
    e: React.MouseEvent<HTMLDialogElement, MouseEvent>
  ) => {
    const dialog = imageModalRef.current;
    if (imageModalRef.current && e.target == dialog) {
      setOpenedImageSrc(null);
    }
  };

  // when openedImageSrc state changes, either show the modal
  // or close it.
  useEffect(() => {
    if (openedImageSrc) {
      imageModalRef.current?.showModal();
    } else {
      imageModalRef.current?.close();
    }
  }, [openedImageSrc]);

  return (
    <>
      {openedImageSrc && (
        <dialog
          ref={imageModalRef}
          className="modal"
          onCancel={() => setOpenedImageSrc(null)}
          onClick={handleModalOutsideClose}
          id="image_modal"
        >
          <div className="modal-box">
            <form method="dialog" className="modal-backdrop ">
              <button
                onClick={() => setOpenedImageSrc(null)}
                className="btn btn-sm btn-circle absolute"
              >
                ✕
              </button>
            </form>
            <Image
              src={openedImageSrc}
              width={450}
              height={450}
              alt="product"
              className="place-self-center"
            />
          </div>
        </dialog>
      )}
    </>
  );
}
